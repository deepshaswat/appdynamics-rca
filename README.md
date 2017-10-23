# appdynamics-rca
This repository an attempt to write a tool that can take metric paths of an application on Appdynamics Controller as input and find possible correlations between the metrics.

## How to Run

 - Add metric paths in the file `metrics` without the URL.
 
 - Run:
```
python rca.py <controller_url> <username@account_name> <password>
```

It will give pearsonr coeffiecient as output for all pairs. 

## TODO
- Test better non-linear correlation coefficients.
- Break metric value lists into subarrays and try to find correlations
