from IPython.core.display import Image

from common.lib.plantuml import PlantUML, PlantUMLHTTPError


def plant_uml_image(code: str) -> Image:
    try:
        encoded = PlantUML(url="https://www.plantuml.com/plantuml/img/").processes(code)
        return Image(data=encoded)
    except PlantUMLHTTPError as e:
        print(e)
        return Image(data=e.content)
