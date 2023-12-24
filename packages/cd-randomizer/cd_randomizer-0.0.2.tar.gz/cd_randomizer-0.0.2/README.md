
# cd_randomizer

`cd_randomizer` is a Python package for randomizing CDs.

## Installation

You can install `cd_randomizer` using pip:

```bash
pip install cd_randomizer
```

## Usage

Here is a simple example of how to use `cd_randomizer`:

```python
from cd_randomizer.rand import Randomizer as rando

a_list = [1,2,3,4,5]

# Example usage
item = rando.random_list_item(a_list)
print("random item", item)

rando.randomize_list(a_list) # it will shuffle in place, no nee to make another list
print(a_list)

decimal = rando.random_decimal(2.50005, 4.0, round_to=3)
print("random decimal(float)", decimal)

list_item = rando.random_list_item(a_list)
print("random list item", list_item)

rand_number = rando.random_number(1, 100)
print("Random whole number between 1 and 100", rand_number)

rand_items = rando.random_sample_of_a_list(a_list, 3)
print("3 random list items", rand_items)
```

## Examples

For more examples, please refer to the `examples` folder.

## Contributing

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

## More documentation at:
[Code Docta](https://codedocta.com "Code Docta")

## License

[MIT](https://choosealicense.com/licenses/mit/)
