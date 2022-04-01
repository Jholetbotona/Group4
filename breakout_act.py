import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "1TvUJEZQVdbj7gikUoNgfUemKXcOlIUj"



############### CLASS HERE, let's try to create more functions for functionality
class Conversion:
    def __init__(self):### Created indexes to easily call out the values
        self.x = input("KM, M or miles format: ") #Choose what imperial or metric system you want to see
        self.Paths = ["Fastest","Shortest","Pedestrian","Bicycle"] #Choose path
        self.Avoids = ["Highways","Toll Road","Ferry","Unpaved","Approximate Seasonal Closure","Country Border Crossing","Bridge","Tunnel"]
        self.Choices()
    def main(self):
        if self.x == "km" or self.x == "KM" or self.x == "Km" or self.x == "kM":
            y = " km"
        elif self.x == "m" or self.x == "M":
            y = " m"
        elif self.x == "miles" or self.x == "Miles" or self.x == "MILES" or self.x == "mi" or self.x == "Mi" or self.x == "mI" or self.x == "MI":
            y = " mi"
        self.y = y
        return self.y
    ### This is where the choices are created
    def Choices(self):
        print("What path do you want to take?\n")
        for i in range(len(self.Paths)):
            print("[" +str(i+1) + "] {}\n".format(self.Paths[i]))
        self.Path=int(input())### For loop to easily create Choices
        print("What do you want to avoid\n")
        for i in range(len(self.Avoids)):
            print("[" +str(i+1) + "] {}\n".format(self.Avoids[i]))
        self.Avoid=int(input())
        return self.Path,self.Avoid
while True:
    z = Conversion()
    orig = input("Starting Location: ")
    if orig == "quit" or orig == "q":
        break
    dest = input("Destination: ")
    if dest == "quit" or dest == "q":
        break
    ###Added parameters, z.Paths[z.Path] indicicates value taken from class self.Paths and z.Path is its place.
    url = main_api + urllib.parse.urlencode({"key":key, "from":orig, "to":dest,"routeType":z.Paths[z.Path-1],"avoids":z.Avoids[z.Avoid-1]})
    json_data = requests.get(url).json()
    print("URL:"+(url))
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        print("API Status:"+str(json_status)+"=A successful route call.\n")
        print("=============================================")
        print("Directions from " + (orig) + " to " + (dest))
        print("Trip Duration:   " + (json_data["route"]["formattedTime"]))
        ############ I've added selection whether to pick from Kilometers or Meters
        if z.x == "km":
            print("Kilometers:      " + str("{:.2f}".format((json_data["route"]["distance"])*1.61) + str(z.main())))
        elif z.x == "m":
            print("Meters:      " + str("{:.2f}".format(((json_data["route"]["distance"])*1.61)*1000) + str(z.main())))#### Multiply the output of KM to 1k in order to produce Meters
        elif z.x == "miles" or z.x == "Miles" or z.x == "MILES":
            print("Miles:      " + str("{:.2f}".format(((json_data["route"]["distance"])*1.61)*.621371) + str(z.main())))### Multiply the output of KM to .621371 in order to produce miles
        print("Fuel Used (Ltr): " + str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78)))
        print("=============================================")
        if z.x == "km":
            for each in json_data["route"]["legs"][0]["maneuvers"]:
                print((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + str(z.main()+ ")")))
        elif z.x == "m":
            for each in json_data["route"]["legs"][0]["maneuvers"]:
                print((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61*1000) + str(z.main() + ")")))
        elif z.x == "miles" or z.x == "Miles" or z.x == "MILES":
            for each in json_data["route"]["legs"][0]["maneuvers"]:
                print((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61*.621371) + str(z.main()+ ")")))
        print("Fuel Used (Ltr): " + str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78)))
        
        print("=============================================\n")
    elif json_status == 402:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
        print("**********************************************\n")
    elif json_status == 611:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
        print("**********************************************\n")
    else:
        print("************************************************************************")
        print("For Staus Code: " + str(json_status) + "; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print("************************************************************************\n")