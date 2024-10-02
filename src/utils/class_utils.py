def get_all_derived_classes(base_class):
    derived_classes = []
    for subclass in base_class.__subclasses__():
        derived_classes.append(subclass)
        derived_classes.extend(get_all_derived_classes(subclass))
    return derived_classes