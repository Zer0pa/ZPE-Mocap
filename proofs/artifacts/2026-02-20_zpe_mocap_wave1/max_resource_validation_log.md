# Max Resource Validation Log

## Environment Bootstrap
### Shell bootstrap attempt
- command: `zsh -lc set -a; [ -f .env ] && source .env; set +a; echo BOOTSTRAP_OK`
- exit_code: `0`
- timed_out: `False`
- stdout_tail:
```text
BOOTSTRAP_OK

```

## Resource Attempts

### Kaiwu arXiv access
- command: `curl -L https://arxiv.org/abs/2503.05231 -o /Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/artifacts/2026-02-20_zpe_mocap_wave1/tmp/kaiwu_arxiv.html`
- exit_code: `0`
- timed_out: `False`
- stderr_tail:
```text
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100 46665  100 46665    0     0  96286      0 --:--:-- --:--:-- --:--:-- 96614

```

### BABEL header probe
- command: `curl -I https://babel.is.tue.mpg.de/`
- exit_code: `0`
- timed_out: `False`
- stdout_tail:
```text
-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=63072000; includeSubdomains;
X-Permitted-Cross-Domain-Policies: none
X-Content-Type-Options: nosniff
Permissions-Policy: geolocation=();midi=();notifications=();push=();sync-xhr=();microphone=();camera=();magnetometer=();gyroscope=();speaker=(self);vibrate=();fullscreen=(self);payment=();
Accept-Ranges: bytes


```
- stderr_tail:
```text
rent
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0 13103    0     0    0     0      0      0 --:--:--  0:00:01 --:--:--     0
  0 13103    0     0    0     0      0      0 --:--:--  0:00:01 --:--:--     0

```

### BABEL landing page
- command: `curl -L https://babel.is.tue.mpg.de/ -o /Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/artifacts/2026-02-20_zpe_mocap_wave1/tmp/babel_home.html`
- exit_code: `0`
- timed_out: `False`
- stderr_tail:
```text
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100 13103  100 13103    0     0  14166      0 --:--:-- --:--:-- --:--:-- 14196

```

### BABEL dependency setup (smplx)
- command: `/Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/.venv/bin/python -m pip install smplx`
- exit_code: `1`
- timed_out: `False`
- stdout_tail:
```text
1.0.1.post2
    smplx 0.1.11 depends on torch>=1.0.1.post2
    smplx 0.1.10 depends on torch>=1.0.1.post2

Additionally, some packages in these conflicts have no matching distributions available for your environment:
    torch

To fix this you could try to:
1. loosen the range of package versions you've specified
2. remove package versions to allow pip to attempt to solve the dependency conflict


```
- stderr_tail:
```text
3, smplx==0.1.14, smplx==0.1.15, smplx==0.1.16, smplx==0.1.17, smplx==0.1.20, smplx==0.1.21, smplx==0.1.22, smplx==0.1.23, smplx==0.1.24, smplx==0.1.25, smplx==0.1.26, smplx==0.1.27 and smplx==0.1.28 because these package versions have conflicting dependencies.
ERROR: ResolutionImpossible: for help visit https://pip.pypa.io/en/latest/topics/dependency-resolution/#dealing-with-dependency-conflicts

```

### RELI11D arXiv access
- command: `curl -L https://arxiv.org/abs/2403.19501 -o /Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/artifacts/2026-02-20_zpe_mocap_wave1/tmp/reli11d_arxiv.html`
- exit_code: `0`
- timed_out: `False`
- stderr_tail:
```text
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100 47837  100 47837    0     0   111k      0 --:--:-- --:--:-- --:--:--  111k

```

### LAFAN1 repository attempt
- command: `git -C /Users/Zer0pa/ZPE/ZPE Mocap/external/datasets/ubisoft-laforge-animation-dataset pull --ff-only`
- exit_code: `0`
- timed_out: `False`
- stdout_tail:
```text
Already up to date.

```

### CMU site header probe
- command: `curl -I http://mocap.cs.cmu.edu`
- exit_code: `0`
- timed_out: `False`
- stdout_tail:
```text
HTTP/1.1 200 OK
date: Fri, 20 Mar 2026 18:00:57 GMT
server: Apache/2.4.61 (FreeBSD)
x-powered-by: PHP/8.3.8
content-type: text/html; charset=UTF-8
Connection: keep-alive


```
- stderr_tail:
```text
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:--  0:00:01 --:--:--     0
  0     0    0     0    0     0      0      0 --:--:--  0:00:01 --:--:--     0

```

### CMU site fetch
- command: `curl -L http://mocap.cs.cmu.edu -o /Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/artifacts/2026-02-20_zpe_mocap_wave1/tmp/cmu_home.html`
- exit_code: `0`
- timed_out: `False`
- stderr_tail:
```text
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100  8445    0  8445    0     0  14188      0 --:--:-- --:--:-- --:--:-- 14217
100  8445    0  8445    0     0  14185      0 --:--:-- --:--:-- --:--:-- 14217

```

### CMU commercial-safe BVH mirror attempt
- command: `git -C /Users/Zer0pa/ZPE/ZPE Mocap/external/datasets/cmu-mocap pull --ff-only`
- exit_code: `None`
- timed_out: `True`

### Mixamo header probe
- command: `curl -I https://www.mixamo.com`
- exit_code: `0`
- timed_out: `False`
- stdout_tail:
```text
s://bam.nr-data.net https://*.newrelic.com https://assets.adobedtm.com https://*.cloudfront.net  'unsafe-inline' 'unsafe-eval' 'self'
X-Xss-Protection: 1
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Accept-Ranges: bytes
Cache-Control: public, max-age=0
Last-Modified: Thu, 05 Feb 2026 02:21:24 GMT
Etag: W/"8f5b-19c2b9ab369"
X-Request-Id: RmXq5Ll0cVyUn2BfIQBFEIEdbiQesMFo


```
- stderr_tail:
```text
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0 36699    0     0    0     0      0      0 --:--:--  0:00:01 --:--:--     0

```

### Mixamo landing fetch
- command: `curl -L https://www.mixamo.com -o /Users/Zer0pa/ZPE/ZPE Mocap/ZPE-Mocap/proofs/artifacts/2026-02-20_zpe_mocap_wave1/tmp/mixamo_home.html`
- exit_code: `0`
- timed_out: `False`
- stderr_tail:
```text
rent
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:--  0:00:01 --:--:--     0
100 36699  100 36699    0     0  23517      0  0:00:01  0:00:01 --:--:-- 23540

```

## Kaiwu multimodal mocap+bio
- attempted: `True`
- success: `False`
- claims: `MOC-C001, MOC-C005, MOC-C007`
- impracticality: `IMP-ACCESS`
- failure_signature: No dataset/code endpoint surfaced on fetched Kaiwu page
- fallback: Proxy multimodal alignment report
- claim_impact: Kaiwu-linked claims cannot be promoted and remain explicit FAIL/PAUSED_EXTERNAL

## BABEL (AMASS)
- attempted: `True`
- success: `False`
- claims: `MOC-C001, MOC-C002, MOC-C006`
- impracticality: `IMP-LICENSE`
- failure_signature: BABEL/AMASS download path appears account/license gated
- fallback: Action-labeled synthetic corpus with deterministic labels
- claim_impact: BABEL-linked max-wave comparator remains blocked by license gating

## RELI11D
- attempted: `True`
- success: `False`
- claims: `MOC-C003, MOC-C004, MOC-C007`
- impracticality: `IMP-ACCESS`
- failure_signature: No repository/data endpoint found on RELI11D source page
- fallback: Synthetic multi-sensor stress corpus
- claim_impact: RELI11D-linked claims cannot be promoted without accessible source

## LAFAN1 baseline
- attempted: `True`
- success: `True`
- claims: `MOC-C001, MOC-C002, MOC-C003`

## CMU Mocap baseline
- attempted: `True`
- success: `True`
- claims: `MOC-C001, MOC-C002, MOC-C003`

## Mixamo retarget alternative
- attempted: `True`
- success: `False`
- claims: `MOC-C006`
- impracticality: `IMP-ACCESS`
- failure_signature: Mixamo asset export is account-gated
- fallback: Use CMU-derived transformed skeletons for retarget stress
- claim_impact: Mixamo blocked; CMU commercial-safe substitute used for MOC-C006 closure

