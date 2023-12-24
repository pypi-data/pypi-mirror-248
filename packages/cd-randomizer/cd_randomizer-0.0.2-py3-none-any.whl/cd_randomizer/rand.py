import random


class Randomizer:
    @staticmethod
    def random_decimal(min_decimal, max_decimal, round_to=None):
        """
        Generate a random decimal number between min_decimal and max_decimal.

        Args:
            min_decimal (float): The minimum value for the decimal.
            max_decimal (float): The maximum value for the decimal.
            round_to (int, optional): Number of decimal places to round to.
                                      If None, no rounding is performed. Defaults to None.

        Returns:
            float: A random decimal number, optionally rounded to a specified number of decimal places.
        """
        decimal = random.uniform(min_decimal, max_decimal)
        return round(decimal, round_to) if round_to else decimal

    @staticmethod
    def randomize_list(your_list):
        """
        Shuffle the elements of a given list in place.

        Args:
            your_list (list): The list to be shuffled.

        Returns:
            None: The list is modified in place and nothing is returned.
        """
        random.shuffle(your_list)

    @staticmethod
    def random_list_item(your_list):
        """
        Select a random item from a given list.

        Args:
            your_list (list): The list from which to select an item.

        Returns:
            Any: A randomly selected item from the list.
        """
        return random.choice(your_list)

    @staticmethod
    def random_number(min_number, max_number):
        """
        Generate a random integer between min_number and max_number, inclusive.

        Args:
            min_number (int): The minimum integer value.
            max_number (int): The maximum integer value.

        Returns:
            int: A random integer between min_number and max_number.
        """
        return random.randint(min_number, max_number)

    @staticmethod
    def random_sample_of_a_list(your_list, quantity):
        """
        Generate a random sample from a list.

        Args:
            your_list (list): The list to sample from.
            quantity (int): The number of items to sample from the list.

        Returns:
            list: A list of sampled items.
        """
        return random.sample(your_list, quantity)
