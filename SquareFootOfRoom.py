print("Enter the dimensions of your room in sqft")


def calculate_area(w, h):
    area_sqft = w * h
    print(f"The total sqft is: {area_sqft}")


width = int(input("Enter the width of your room: "))
height = int(input("Enter the height of your room: "))

calculate_area(width, height)
