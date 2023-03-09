# Comparing Different Evolutionary Algorithms

This final project compares different evolutionary algorithms to see which can develop the best creatures for locomotion.

This project used a total of (3 evolutionary algorithms) x (5 trials/evolutionary algorithm) x (200 generations/trial) x (25 individuals/generation) = **75,000 SIMULATIONS!!!**


<br/>


## Running the code

This program allows you to run various different evolutionary algorithms.

To run a **Parallel Hill Climber**, simply type:

```bash
$ python3 search.py phc
```

To run the **(μ,λ) Evolutionary Algorithm**, simply type:

```bash
$ python3 search.py ml
```

To run **Age-Fitness Pareto Optimization**, simply type:

```bash
$ python3 search.py afpo
```


<br/>


## Demo

An exampled of a randomly generated creature vs. a creature evolved using each of these evolutionary algorithms can be seen [here](https://youtu.be/V1Dc-OBX-d0).


<br/>


# Fitness Function

The fitness function is the negative x-position of the first link. The farther left (negative x-direction) the creature travels, the higher its fitness value. The goal of this fitness function is to evolve locomotion in our creatures.
<br/>
<br/>
When testing these algorithms for many generations, the evolutionary algorithm eventually exploited the physics simulator by embedding itself in the ground, which launches the creature upwards at an angle and results in a large displacement in the x-direction. To penalize this behavior, if the body's z-height exceeds 4 at any point during the simulation, the fitness of the creature is set to -5. Such a fitness value is usually low enough for evolution to naturally discard the solution.


<br/>


# Evolutionary Methods

I tested 3 different evolutionary methods. Each method used a population size of 25 and was run for 200 generations. I tested each method 5 times, each with a different random seed.

<br/>

## Parallel Hill Climber

The Parallel Hill Climber starts off with 25 individuals. Each individual is in a "silo," meaning that it does not interact with the other individuals in the population. In each generation, the parents have children, and the parent is compared against its child. Whichever has a higher fitness, the parent or the child, moves on to the next generation.

A simplified illustration of this evolutionary algorithm is shown below:

![Parallel Hill Climber Diagram](images/PHC_Diagram.png "Parallel Hill Climber Diagram")
<br/>

<br/>

## (μ,λ) Evolutionary Algorithm

The (μ,λ) Evolutonary Algorithm has 2 key parameters:
- **μ:** The number of parents chosen to move onto the next generation
- **λ:** The overall size of the population
<br/>

For our experiments, we used **μ = 5** and **λ = 25**, meaning that our population size was 25 and the top 5 individuals in each generation were chosen to move onto the next generation.

Typically, each individual chosen to move onto the next generation would have **λ/μ - 1** offspring. In this case, that would be **25/5 -1 = 4** offspring per parent. This way, the total population would be *5 parents from the previous generation + (4 offspring/parent) x (5 parents) = 5 + 20 = 25 total individuals.* Thus, the population size stays constant throughout the generations.

Unfortunately, this leads to a lack of genetic diversity. In the figure below, each of the starting individuals is given a different color, and every future descendent of that individual is given the same color. From this, we can see that after about the 5th generation, only the yellow lineage prevails and all the other lineages die out. This leads to a lack of genetic diversity, and genetic diversity is very critical for evolution.

![Mu Lambda Vanilla](images/ML_Vanilla.png "Mu Lambda Vanilla")
<br/>

Therefore, I modified this algorithm so that each individual chosen to move onto the next generation would have **λ/μ - 2** offspring. In this case, that would be **25/5 - 2 = 3** offspring per parent. Then, I planted *μ = 5* completely new, random creatures into the population. This way, the total population would be *5 individuals from the previous generation + (3 offspring/parent) x (5 parents) + 5 new/random individuals = 5 + 15 + 5 = 25 total individuals.* Thus, the population size stays constant throughout the generations.

An illustration of this evolutionary algorithm is shown below:

![(μ,λ) Evolutionary Algorithm Diagram](images/ML_Diagram.png "(μ,λ) Evolutionary Algorithm Diagram")
<br/>

<br/>

## Age-Fitness Pareto Optimization

For Age-Pareto Fitness Optimization, I once again began with a population size of 25. From this population, I chose the 12 best individuals through the following process: I gathered the individuals along the Pareto front, which have a Pareto level of 0. If I still don't have 12 individuals, I continue recruiting individuals with a Pareto level of 1, then a Pareto level of 2, and so on until I have a group of 12 individuals.

Next, all of these 12 individuals have a child. At this point we have the 12 best individuals from the previous generation (based on Pareto levels) and each of their children, so *12 + 12 = 24 individuals.* In order to maintain a population size of 25 in each generation, I add one new, randomly generated individual to this group. This way, each generation has 25 individuals: 24 related to the previous generation and 1 brand new creature.


An illustration of this evolutionary algorithm is shown below:

![Age-Fitness Pareto Optimization](images/AFPO_Diagram.png "Age-Fitness Pareto Optimization")
<br/>


### What is a Pareto Front?

An individual is on the Pareto front if there is no other individual in the population that is more fit AND younger than it. In the diagram below, the highlighted region represents the space of both greater fitness AND lower age. Because there are no other individuals in the highlighted region, the individual is considered to be on the Pareto front. The same applies to all of the light blue dots in the plot.

![Pareto Front](images/ParetoFront.png "Pareto Front")
<br/>

### What are Pareto Front?

The Pareto level of an individual is equal to the number of other individual in the population that are more fit AND younger than it. In the diagram below, the highlighted region represents the space of both greater fitness AND lower age. Because there is only 1 individual in the highlighted region, the individual is considered to have a Pareto level of 1.

![Pareto Levels](images/ParetoLevels.png "Pareto Levels")
<br/>

### Why Age-Fitness Pareto Optimization Is Beneficial

The reason this algorithm is so good is that, by introducing random creatures into the population throughout the evolution process, it helps increase genetic diversity. However, introducing a new, randomly generated individual into a population will place it at a disadvantage if you're blindly comparing its fintess against everyone else's fitness. Therefore, we factor in age as well. By selecting for individuals that are non-dominated in both fitness AND age, we are able to give younger creatures a "handicap" if they are pretty fit for their age. In the figure below, each lineage is given a different color. Notice that, at the end of evolution, the red lineage has the highest fitness. However, the red creature is randomly introduced into the population around generation 25. When it is first introduced, its fitness is quite low compared to everyone else in the population at the time. However, because it was pretty fit given its age, the red lineage was allowed to live on until it eventually evolved into the fittest in the population.

![AFPO Advantage](images/AFPO_Advantage.png "AFPO Advantage")
<br/>

<br/>



# Results

The following table lists the best fitness achieved by the end of 200 generations in each of the 5 trials that I ran using each evolutionary algorithm:

| Trial | Parallel Hill Climber | (μ,λ) | Age-Fitness Pareto Optimization |
| --- | --- | --- | --- |
| **Trial 1** | 9.220 | 10.531 | 10.070 |
| **Trial 2** | 9.276 | 8.319  | 10.809 |
| **Trial 3** | 8.750 | 4.345  | 10.169 |
| **Trial 4** | 9.344 | 8.141  | 10.083 |
| **Trial 5** | 9.508 | 8.169  | 10.297 |
| **Average** | 9.220 | 7.901  | 10.286 |

<br/>

On average, the Age-Pareto Fitness Optimization produces the fittest creature. Surprisingly, the Parallel Hill Climber produced more consistent results and a higher average fitness than the (μ,λ) Evolutionary Algorithm.

Plots from all 15 trials (5 for each evolutionary algorithm) are shown below.

### Parallel Hill Climber

*How to interpret the graphs:* Each line represents a separate hill climber. For a parallel hill climber with a population size of 25, there are 25 separate hill climbers evolving in parallel.

![Parallel Hill Climber Trial 1](images/PHC%20Plot%201.png "Parallel Hill Climber Trial 1")
<br/>
![Parallel Hill Climber Trial 2](images/PHC%20Plot%202.png "Parallel Hill Climber Trial 2")
<br/>
![Parallel Hill Climber Trial 3](images/PHC%20Plot%203.png "Parallel Hill Climber Trial 3")
<br/>
![Parallel Hill Climber Trial 4](images/PHC%20Plot%204.png "Parallel Hill Climber Trial 4")
<br/>
![Parallel Hill Climber Trial 5](images/PHC%20Plot%205.png "Parallel Hill Climber Trial 5")
<br/>
<br/>

### (μ,λ) Evolutionary Algorithm
*How to interpret the graphs:* Each line represents an individual over the course of evolution. If the individual has a child, the child stems off from its parent line in a new color. If a line randomly begins in the middle of the plot (i.e. it's not branching off another line), that line represents a randomly generated solution. If a line ends randomly, it means that the individual was not fit enough to survive.

![(μ,λ) Trial 1](images/ML%20Plot%204.png "(μ,λ) Trial 1")
<br/>
![(μ,λ) Trial 2](images/ML%20Plot%201.png "(μ,λ) Trial 2")
<br/>
![(μ,λ) Trial 3](images/ML%20Plot%202.png "(μ,λ) Trial 3")
<br/>
![(μ,λ) Trial 4](images/ML%20Plot%203.png "(μ,λ) Trial 4")
<br/>
![(μ,λ) Trial 5](images/ML%20Plot%205.png "(μ,λ) Trial 5")
<br/>
<br/>

### Age-Pareto Fitness Optimization
*How to interpret the graphs:* Each line represents an individual over the course of evolution. If the individual has a child, the child stems off from its parent line in a new color. If a line randomly begins in the middle of the plot (i.e. it's not branching off another line), that line represents a randomly generated solution. If a line ends randomly, it means that the individual was not fit enough to survive.

![AFPO Trial 1](images/AFPO%20Plot%201.png "AFPO Trial 1")
<br/>
![AFPO Trial 2](images/AFPO%20Plot%202.png "AFPO Trial 2")
<br/>
![AFPO Trial 3](images/AFPO%20Plot%203.png "AFPO Trial 3")
<br/>
![AFPO Trial 4](images/AFPO%20Plot%204.png "AFPO Trial 4")
<br/>
![AFPO Trial 5](images/AFPO%20Plot%205.png "AFPO Trial 5")
<br/>
<br/>


# Creature Morphology

## Creature Bodies

The information for each body is organized in a randomly generated tree. An example of such a randomly generated tree is shown below.
<br/>
<br/>
![Body Tree](images/body_tree_with_text.PNG "Body Tree")
<br/>
<br/>


Each node of the tree represents a link (rectangular prism) on the body. A link contains the following information:
<br/>
<br/>
![Link Diagram](images/link_diagram.PNG "Link Diagram")
<br/>
<br/>


| Variable | Description | Value |
| --- | --- | --- |
| index | A unique integer assigned to each link in the tree | An integer in the range [0, n-1], where n is the number of links in the tree |
| length | The length of the link | A randomly generated number in the range [0.2, 1.2] |
| width | The width of the link | A randomly generated number in the range [0.2, 1.2] |
| height | The height of the link | A randomly generated number in the range [0.2, 1.2] |
| hasSensor | A boolean indicating whether or not the link has a sensor | True or False |
| jointPos | Indicates where the link is attached to its parent (12 possible attachment configurations) | An integer in the range [0,11] |
| jointAxis | Indicates the axis of the joint | "1 0 0", "0 1 0", or "0 0 1" |
| depth | The depth of the link in the tree. This is sort of an "inverse depth," as the bottom-most link has a depth of 1. | An integer in the range [1, n], where n is the total depth of the tree |
| totalDepth | The total depth of the body tree | An integer in the range [2, 5] |
| children | A list of direct child links | The root node can have 1-4 child links, while all other nodes can only have 0 or 1 |
| linksBelow | A list containing the link's own index as well as all the indices of it descendent links | List of link indices |
| linksWithSensors | A dictionary whose keys are the indices of all the descendent links that have sensors (including its own index if it has a sensor). The associated values are randomly generated weights in the range [-1, 1] | Dictionary with link indices as keys and random numbers in the range [-1, 1] as values |

<br/>

__Note 1:__ Each node's *linksWithSensors* dictionary has unique weights corresponding to each sensor.
<br />
__Note 2:__ The root node's *linksBelow* array is a list of every node in the tree, as everything is a descendent of the root node.
<br />
__Note 3:__ The keys in the root node's *linksWithSensors* dictionary encompasses every link that has a sensor in the tree.


<br/>


## Creature Brains

### Locations of Sensors

Whether or not each block has a sensor is randomly determined. Blocks with sensors are colored green, while blocks without sensors are colored blue.

### Local Brain

All of the information for the brain is contained within the link nodes. Most of this data is stored within the *linksWithSensors* dictionaries, which contain link indices as keys and weights as the corresponding values. When a link is added or removed, this change is propagated through the tree by altering the relevant *linksWithSensors* dictionaries.

When generating the brain, only the links with sensors are given sensor neurons (a list of such links is contained within the keys of the root node's *linksWithSensors* dictionary). However, all joints are given motor neurons. The activation of each motor neuron is a weighted sum of all the sensor values of its descendent links. The associated weights are taken from the *linksWithSensors* dictionary of the joint's child link. An example of this is shown below.
<br/>
<br/>
![Local Brain Layout](images/local_brain_diagram.PNG "Local Brain Layout")
<br/>
![Local Brain Math](images/local_brain_math.PNG "Local Brain Math")
<br/>
<br/>


__Neuron Naming Convention:__
- The name of a motor neuron is the index of the joint's child link.
- The names of a sensor neuron is equal to the index of the link + 100, in order to prevent overlap with the names of motor neurons.


<br/>


## Mutations

| Mutation | Description | Probability |
| --- | --- | --- |
| Remove a link | The link and all of its descendent links are removed from the tree. The *linksWithSensors* dictionary and *linksBelow* list belonging to all the ancestor nodes of the removed link are updated accordingly. | 0.1 |
| Add a link | A link is added to the tree. | 0.1 |
| Change link length | The length of the link is changed to a randomly generated number in the range [0.2, 1.2]. | 0.3 |
| Change link width | The width of the link is changed to a randomly generated number in the range [0.2, 1.2]. | 0.3 |
| Change link height | The height of the link is changed to a randomly generated number in the range [0.2, 1.2]. | 0.3 |
| Change joint axis | The joint axis between the link and its parent is changed. | 0.2 |
| Add sensor | A sensor is added to the link if it didn't already have one. | 0.2 |
| Remove sensor | The sensor is removed from the link if it previously had one. | 0.2 |
| Alter synapse weight | The synapse weight is changed to a new value in the range [-1, 1]. | 0.1 |


<br/>


# Note

This is a final project for CS396 (*Artififical Life*) at Northwestern University. This project is based on a massively open online course (MOOC) on reddit called [Ludobots](https://www.reddit.com/r/ludobots/wiki/installation/). It also builds on the Pyrosim library which can be found [here](https://github.com/jbongard/pyrosim).