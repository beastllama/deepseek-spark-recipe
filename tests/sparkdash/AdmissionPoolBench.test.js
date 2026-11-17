import { test } from 'node:test';
import assert from 'node:assert/strict';
import http from 'node:http';
import { validateCachedTail, validateAdmissionCapacity, runCachedTailScenario } from '../CachedTailBench.js';

test('pool comparison requires the two exact pools and logical context', () => {
  assert.equal(validateCachedTail('admission-pool'), 'admission-pool');
  assert.throws(() => validateCachedTail('admission-pool', true));
  for (const pool of [655360, 786432]) validateAdmissionCapacity(pool, 524288, 'admission-pool');
  assert.throws(() => validateAdmissionCapacity(655360, 655360, 'admission-pool'));
  assert.throws(() => validateAdmissionCapacity(524288, 524288, 'admission-pool'));
});

test('pool wave matches long and short work and rejects unverifiable samples', { timeout: 15000 }, async t => {
  const tails = [1024, 2048, 4096, 8192];
  const prime = 133344;
  let outstanding = 0, completed = 0, caseName = 'match', sawFour = false, shortCalls = 0;
  let bodyLog = [];
  let earlyFirstFinished = Promise.resolve(), settleEarlyFirst = () => {};
  const server = http.createServer(async (req, res) => {
    if (req.url === '/metrics') {
      const waiting = outstanding >= 4 ? 1 : 0;
      if (outstanding === 4 && !shortCalls) sawFour = true;
      return res.end([
        'tensorfold:requests_running ' + (outstanding - waiting),
        'tensorfold:requests_waiting ' + waiting,
        'tensorfold:request_latency_seconds_count ' + completed,
        'tensorfold:client_disconnections_total 0',
        '',
      ].join('\n'));
    }

    let data = '';
    for await (const chunk of req) data += chunk;
    const body = JSON.parse(data);
    bodyLog.push(body);
    const isPrime = body.max_tokens === 8;
    const longIndex = Number(body.messages[0].content.match(/\nContinuation ([1-4])\./)?.[1] ?? 0) - 1;
    const isShort = !isPrime && longIndex < 0;
    if (isShort) {
      assert.ok(sawFour, 'short dispatch follows metric proof');
      shortCalls++;
    }
    if (caseName === 'early' && longIndex > 0) await earlyFirstFinished;
    outstanding++;
    res.setHeader('content-type', 'text/event-stream');
    res.write('data: ' + JSON.stringify({ choices: [{ delta: { reasoning_content: 'Checking.' } }] }) + '\n\n');
    const duration = isPrime ? 20 : caseName === 'early' && longIndex === 0 ? 5 : 320;
    setTimeout(() => {
      let tokens = isPrime ? prime : isShort ? 512 : prime + tails[longIndex];
      if (!isPrime && !isShort && longIndex === 3 && caseName === 'geometry') tokens -= 2048;
      const usage = {
        prompt_tokens: tokens,
        completion_tokens: 12,
        prompt_tokens_details: { cached_tokens: isPrime ? 0 : isShort ? (caseName === 'warm-short' ? 128 : 0) : prime - 96 },
      };
      outstanding--;
      completed++;
      res.end('data: ' + JSON.stringify({ choices: [{ delta: { content: 'Check the backup.' }, finish_reason: 'stop' }], usage }) + '\n\ndata: [DONE]\n\n');
      if (isShort && caseName === 'outside') completed++;
      if (caseName === 'early' && longIndex === 0) settleEarlyFirst();
    }, duration);
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  t.after(() => { server.closeAllConnections(); server.close(); });
  const options = { baseUrl: 'http://127.0.0.1:' + server.address().port, modelId: 'fixture', mode: 'admission-pool', salt: 'pool-offline' };
  const result = await runCachedTailScenario(options);
  assert.equal(result.error, null);
  assert.equal(result.concurrency, 5);
  assert.equal(result.streams.length, 6);
  assert.equal(result.samples[0].comparisonValid, true);
  assert.equal(result.samples[0].completedRequests, 5);
  assert.equal(result.samples[0].traffic.submitted, 6);
  assert.equal(result.samples[0].shortArrival.running, 3);
  assert.equal(result.samples[0].shortArrival.waiting, 1);
  assert.deepEqual(result.samples[0].geometry, {
    longReservations: [167936, 169984, 172032, 176128],
    longReservedTokens: 686080, shortReservedTokens: 34816, totalReservedTokens: 720896,
    threeLongAndShort: 552960,
  });
  assert.equal(shortCalls, 1);
  assert.equal(bodyLog[0].max_tokens, 8);
  for (const body of bodyLog.slice(1)) {
    assert.equal(body.max_tokens, 32768);
    assert.equal(body.reasoning_effort, 'high');
    assert.equal(body.temperature, 0.7);
    assert.equal(body.top_k, 20);
    for (const name of ['min_tokens', 'ignore_eos', 'stop']) assert.equal(name in body, false);
  }
  for (const row of result.streams) assert.equal('contentPreview' in row, false);

  for (const invalid of ['geometry', 'warm-short', 'outside', 'early']) {
    caseName = invalid;
    shortCalls = 0;
    sawFour = false;
    bodyLog = [];
    if (invalid === 'early') earlyFirstFinished = new Promise(resolve => { settleEarlyFirst = resolve; });
    const rejected = await runCachedTailScenario(options);
    assert.ok(rejected.error, invalid);
    assert.equal(rejected.samples[0].comparisonValid, false, invalid);
    assert.equal(rejected.samples[0].discarded, true, invalid);
    if (invalid === 'early') assert.equal(shortCalls, 0);
  }
});
