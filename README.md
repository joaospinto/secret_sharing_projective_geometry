# Introduction

This program implements a secret-sharing scheme using projective geometry (specifically, vector fields over Z_p).
Note that I wrote this a long time ago and the code quality is definitely lacking, but I figured it would be better to have this on my GitHub than rotting away in my hard drive.

# Running

You can run this program with `python3 main.py`.

You'll be asked to specify a few parameters:
- the number of people who will divide the secret;
- the number of people required to reveal the secret;
- a lower bound on the number of values the secret may take.

Next, you will be asked whether you want to encrypt (options 1/2) or decrypt (option 3). Note that option 2 performs some sanity checks that are skipped in option 1, but option 2 should be preferred when possible.

If you pass parameters `4, 2, 20, 1, 3` (run encryption mode with `4` people, with `2` being sufficient to reveal the secret, with `5` possible secret values, and the value being `3`), one possible output would be:
`[[Zp(7), Zp(6), Zp(18)], [Zp(6), Zp(4), Zp(3)], [Zp(10), Zp(4), Zp(22)], [Zp(9), Zp(7), Zp(1)]]`.

To decrypt this, you can specify the parameters `4, 2, 20, 3`, and pass any two secret pieces, e.g. `[Zp(0), Zp(3), Zp(0)], [Zp(0), Zp(2), Zp(0)]]`. You'll get the same secret `3` as the output.
