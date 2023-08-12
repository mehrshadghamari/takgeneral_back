def get_variant_with_min_final_price(variants):
    min_final_price = float("inf")
    selected_variant = None

    for variant in variants:
        if variant.final_price is not None and variant.final_price < min_final_price:
            min_final_price = variant.final_price
            selected_variant = variant

    return selected_variant

def get_variant_with_max_discount(variants):
    max_discount = float("-inf")
    selected_variant = None

    for variant in variants:
        if variant.discount is not None and variant.discount > max_discount:
            max_discount = variant.discount
            selected_variant = variant

    return selected_variant