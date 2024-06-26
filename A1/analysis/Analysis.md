# Analysis of performance of Load Balancer

## A-1

Results of 10000 async requests on N = 3 servers:

![Results](A-1.png)

In the various tests we ran on the system, we found that more requests seemed to be skewed to one of the servers for the given hash-functions. However occasionally the load was balanced somewhat due to the consistent hashing data structure.

### Observation
We observe that the requests per server are not uniform across the servers, as the consistent hashing data structure is not able to balance the load across the servers, this is mainly due its inability to produce completely random numbers, since it is not a pseudo random number generator.

## A-2

Results for various values of N:
<!-- {'989403': 2554, '500494': 7446}
{'422261': 4128, '707281': 2405, '991684': 3467}
{'358773': 4251, '232040': 2998, '666819': 1521, '498061': 1230}
{'491779': 1478, '996199': 1983, '129648': 3496, '822559': 1988, '926487': 1055}
{'130390': 1994, '721951': 2848, '139521': 2047, '319109': 764, '249462': 1732, '476433': 615} -->

<img src="A-2_2.png" alt="drawing" width="150"/>
<img src="A-2_3.png" alt="drawing" width="150"/>
<img src="A-2_4.png" alt="drawing" width="150"/>
<img src="A-2_5.png" alt="drawing" width="150"/>
<img src="A-2_6.png" alt="drawing" width="150"/>

#### Final Plot of Avg. Load and Std. Dev.

<img src="A-2_plot.png" alt="drawing" width="400"/>

### Observation
1. We can see that the average load follows the function (10000/N).
2. However, in such case standard deviation tells a lot about the distribution. In this case for `N = 3` we get the minimum value which tells that for `N = 3`, the distribution is almost uniform.
3. From the line chart we can infer that on increasing the number of servers the uniformity of the distribution improves.


### Hash-Functions:
    phi(i, j) = i^2 + j^2 + 2*j + 25
    
    H(i) = i*2 + 2*i + 17

## A-3

Screen capture of the working:

[![Watch the video](https://img.youtube.com/vi/Fy7rTV35gZc/maxresdefault.jpg)](https://youtu.be/Fy7rTV35gZc)

## A-4

Results for various values of N:
<!-- {'735386': 6598, '386925': 3402}
{'799024': 2307, '364428': 6740, '801449': 953}
{'248218': 4533, '811261': 2560, '621471': 1625, '694817': 1282}
{'958883': 893, '629242': 3709, '858846': 3089, '594252': 814, '456300': 1495}
{'275154': 1710, '965412': 2354, '589207': 1864, '465655': 3162, '678576': 701, '554001': 209} -->

<img src="A-4_2.png" alt="drawing" width="150"/>
<img src="A-4_3.png" alt="drawing" width="150"/>
<img src="A-4_4.png" alt="drawing" width="150"/>
<img src="A-4_5.png" alt="drawing" width="150"/>
<img src="A-4_6.png" alt="drawing" width="150"/>

#### Final Plot of Avg. Load and Std. Dev.

[<img src="A-4_plot.png" alt="drawing" width="400"/>]

### Observation
1. We can see that the average load follows the function (10000/N).
2. However, in such case standard deviation tells a lot about the distribution. In this case for `N = 6` we get the minimum value which tells that for `N = 6`, the distribution is almost uniform.
3. From the line chart we can infer that on increasing the number of servers the uniformity of the distribution improves.
4. The alternate hash functions ensure a better distribution of values leading to more uniform load-balancing with higher number of servers.

### Hash-Functions:
    phi(i, j) = i^3 + 2*i + 15*j + 17
    
    H(i) = 5*i + 21