import re


class Template:

    def __init__(self, html):
        self.html = html

    def get_data(self, data, key):
        keys = key.split('.')
        value = ""
        for key in keys:
            value = data.get(key)
            data = value
        return str(value)

    def render(self, data):

        def parse_block(matched):
            sub_html = matched.group("sub_html")
            sub_key = matched.group("sub_key")
            items = data.get(matched.group("items"))

            results = []
            for item in items:
                sub_data = data.copy()
                sub_data.update({sub_key: item})
                results.append(Template(sub_html).render(sub_data))
            return "".join(results)

        self.html = re.sub('\{\%\s*for\s+(?P<sub_key>\w+)\s+in\s+(?P<items>\w+)\s*\%\}(?P<sub_html>.+)\{\%.+?\%\}',
                           parse_block,
                           self.html,
                           flags=re.S | re.M)

        def parse_inline(matched):
            key = matched.group("key")
            return self.get_data(data, key)

        self.html = re.sub('\{\s*(?P<key>.+?)\s*\}', parse_inline, self.html, flags=re.S | re.M)
        return self.html


if __name__ == '__main__':
    html = """
        <p>Welcome, {name}!</p>
        <p>Products:</p>
        {% for product in product_list %}
            <li>{ product.name }:
                { product.price }</li>
        {% endfor %}
    """
    output = Template(html).render(
            {"name": "hello", "product_list": [{"name": "noodles", "price": 12.1}, {"name": "rice", "price": 12}]})
    print(output)
