# 2048 Bot

An unsuccessful attempt at beating 2048 with openai, stable-baselines

## References

Used this [link] api. However the game was broken, so had to fix it first. Also added some functionality to ease automate playing it



# TO DO

have ugly looking code and comments that needs to be deleted/refactored

## Notes
env stops with a huge penalty if too many idle steps are taken
I had to do this because I couldn't figure out how to change action space on the run.

I believe one of the many problems of the model is that it can't handle idle actions well which deteriorates the learning a lot.

Not all models are supported


Can add another layer of observation that looks ahead and decides idle actions. But once one starts looking ahead, what's the point of using RL in this problem? 