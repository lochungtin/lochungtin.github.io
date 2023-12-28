# Bachelor's Final Year Project

![logo](./bsc.png ':size=25%')

## Introduction

In this extensive report, I embarked on the development and analysis of various ghost agent variants within the Pac-Man game environment. I conducted experiments using different approaches, including deep Q-learning, neuroevolution, and temporal difference learning. Throughout my experiments, I delved into the performance of various ghost agent combinations in the Pac-Man game. The diverse variants, including _hyper-aggressive_, _MDP-based_, _TD learning_, and _neuroevolutionary agents_, were meticulously tested and analysed.

<div style="text-align:center">

![logo](./bsc-pacman.png ':size=WIDTHxHEIGHT')

</div>

## Analysis

The experimentation involved detailed analysis, including metrics such as _completion percentage_, _timesteps per game_, and _death tally_. The results consistently showed that combinations involving **neuroevolutionary** and **temporal difference learning** ghost variants outperformed others, exhibiting significant improvements in efficiency and Pac-Man capture.

Notably, the analysis indicated that the hyper-aggressive and MDP-based ghost agents posed a greater threat to human players due to their reduced margin of error. However, challenges and limitations arose, primarily stemming from the reduced computational power, lack of human data, and imperfect rewards, impacting the generalisation of results.

# Conclusion

However, my work encountered limitations. Computational constraints forced a reduction in grid size, impacting the generalisation of results to the original Pac-Man game. The absence of human data and imperfect rewards further added to the challenges of generalising findings.

Looking forward, I proposed avenues for future work, emphasising the retraining of machine learning-based ghost agents with human data and refined rewards. Additionally, the introduction of convolution or recurrent layers could enhance the versatility of ghost agents, making them more adept at engaging with human players.
