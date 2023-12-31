# LovelyPancake

<img src="https://github.com/Duzduran/lovely-pancake/blob/main/image/lovelypancake.png?raw=true" width="200" height="200">

LovelyPancake is a general-purpose Python package for machine learning, starting with a robust set of tools for image segmentation. It currently features implementations of U-Net-based models with plans to extend into other machine learning domains.


## Installation

To install LovelyPancake, run:

```bash
pip install lovelypancake
```


## Requirements

The package requires Python 3.x and TensorFlow 2.x. Install all dependencies with:
```bash
pip install -r requirements.txt
```


## Current Features

- U-Net model architecture for image segmentation tasks.
- Attention U-Net and Attention Residual U-Net for advanced segmentation needs.
- Modular design for easy customization and extension of model components.
- Pre-built loss functions and metrics commonly used in image segmentation.

## Future Scope

- Expansion to include a wide range of machine learning models beyond image segmentation.
- Utility functions for data preprocessing, augmentation, and evaluation metrics.
- Integration with other machine learning frameworks and tools.

## Usage

To create and use a U-Net model:

```python
from lovelypancake.models import unet

model = unet(input_shape=(256, 256, 3), NUM_CLASSES=2, dropout_rate=0.1, batch_norm=True)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
```

For detailed examples and more advanced usage, see the `Documentation` [Under Progres...].

