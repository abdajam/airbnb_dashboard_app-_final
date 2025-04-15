def format_number(number, decimals=2):
    return f"{number:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")

AIRBNB_COLORS = {
    'primary': '#FF5A5F',
    'secondary': '#00A699',
    'tertiary': '#FC642D',
    'light': '#FFFFFF',
    'dark': '#484848',
    'light_gray': '#767676'
}