# Setup phase

First compile our circuit with circom

`circom three_fact_proplem.circom --r1cs --wasm --sym --inspect`

Constraints can be seen with 

`snarkjs r1cs print three_fact_proplem.r1cs three_fact_proplem.sym`

Next is setup phase. We need to generate CSR. 

First generate tau. Start with powers of tau generation

`snarkjs powersoftau new bn128 4 pot4_0000.ptau -v`

Next add entropy

`snarkjs powersoftau contribute pot4_0000.ptau pot4_0001.ptau -name="1st_cont" -v`

Add public unpredictable random

`snarkjs powersoftau beacon pot4_0001.ptau pot4_beacon.ptau 0102030405060708090a0b0c00 10 -n="Final Beacon"`

Finally

`snarkjs powersoftau prepare phase2 pot4_beacon.ptau pot4_final.ptau -v`

File `pot4_final.ptau` contains information about generated tau

Now generate CRS and parameters alpha, beta, gama, delta. Algo same as for tau

```
snarkjs groth16 setup three_fact_proplem.r1cs pot4_final.ptau three_fac0000.zkey
snarkjs zkey contribute three_fac0000.zkey three_fac0001.zkey -name="Strannik" -v
snarkjs zkey beacon three_fac0001.zkey three_fac_final.zkey 010203040506070809 10 -n="Final Beacon phase2"
snarkjs zkey export verificationkey three_fac_final.zkey verification_key.json
```

Now we have CRS - `three_fac_final.zkey` and verification key - `verification_key.json`.(although It is part of CRS)

# Prover phase

Given the instance I we need to prove that we know w1, w2, w3 such that I = w1 * w2 * w3

Generate w1, w2, w3

`python3 generate_i.py`


`node three_fact_proplem_js/generate_witness.js three_fact_proplem_js/three_fact_proplem.wasm input.json witness.wtns`

Now witness.wtns contain <w1, w2, w3, i>

Generate profe and instance

`snarkjs groth16 prove three_fac_final.zkey witness.wtns proof.json public.json`

`proof.json` contains three curve points
`public.json` contains instance(I) (but actually it contains 4 numbers, why???)

# Verification
Simple

`snarkjs groth16 verify verification_key.json public.json proof.json`

If answer is `snarkJS: OK!` everything is correct
