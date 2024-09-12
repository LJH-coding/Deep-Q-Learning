# Flappy Bird Reinforcement Learning

This project uses reinforcement learning (RL) to train an agent to play the Flappy Bird game. It implements a Q-learning algorithm with a custom environment integrated into the Gymnasium framework.

## Project Overview

The project includes the following components:
- A custom Flappy Bird environment compatible with Gymnasium.
- A Q-learning algorithm implementation for training the agent.
- Evaluation scripts to assess the performance of the trained agent.

## Installation

To run this project, you will need Python 3.8+ and the following packages:

```bash
pip install gymnasium numpy pygame torch tqdm tensorboard
```

Alternatively, you can install the required packages using the requirements.txt file:

```bash
pip install -r requirements.txt
```

## Usage

### Training the Agent

To train the agent, run the train.py script. This script initializes the environment, sets up the Q-learning parameters, and starts the training process:

```bash
python train.py
```

The training progress will be logged, and the Q-table will be saved periodically and at the end of training.

### Evaluating the Agent

After training, you can evaluate the performance of the agent using the evaluate.py script:

```bash
python eval.py
```

This script loads the trained Q-table and runs the agent through several episodes, logging the average and standard deviation of the rewards.

## Custom Environment

The Flappy Bird environment (FlappyBirdEnv) simulates the Flappy Bird game, where an agent controls the bird trying to navigate through a series of pipes without colliding.

Configuration

Configuration parameters for the Q-learning algorithm include:

* `epsilon`: Initial exploration rate.
* `epsilon_decay`: Factor by which the exploration rate decreases.
* `epsilon_min`: Minimum exploration rate.
* `gamma`: Discount factor for future rewards.
* `lr`: Learning rate for Q-learning updates.
* `episodes`: Number of episodes to run during training.

These parameters can be adjusted in the `train.py` script to optimize performance or experiment with different learning strategies.

## TensorBoard Integration

TensorBoard is used for visualizing training progress. To view TensorBoard logs, run:

```bash
tensorboard --logdir=runs
```

Navigate to the displayed URL in your web browser to view the training metrics.
