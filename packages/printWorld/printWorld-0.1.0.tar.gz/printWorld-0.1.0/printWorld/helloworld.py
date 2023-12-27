import logging


def print_name(name):
    logging.basicConfig(level=logging.WARN, filename='../hello_world.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    logging.warning("hell-o-world, now %s knows python", name)


