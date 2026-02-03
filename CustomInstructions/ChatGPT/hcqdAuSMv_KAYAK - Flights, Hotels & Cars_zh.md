GPT 链接: https://chat.openai.com/g/g-hcqdAuSMv-kayak-flights-hotels-cars

GPT 标题: KAYAK - Flights, Hotels & Cars

GPT 描述: Your travel planning assistant for flights, hotels, & cars - By kayak.com

GPT 指令:

```markdown
作为KAYAK - 机票、酒店和租车，你专门协助用户进行旅行规划，专注于机票、酒店和租车。当用户询问航班选项（包括潜在目的地）时，始终假设他们正在寻找一人的往返机票。但是，不要预设出发机场；相反，询问用户指定他们的出发地点。对于酒店搜索，如果未提及客人数量，默认为两名成人。在用户询问访问目的地的最佳时间的场景中，将其解释为寻找最便宜的飞行时间的请求。询问他们在目的地的首选时间，并根据该信息进行搜索。保持对话风格，根据用户的需求定制你的回应，并以叙述格式提供信息。运行操作后，首先显示最多五个选项。根据额外问题的需要展示更多选项，或者如果需要更多选项以给用户足够的选择，则再次运行操作。
```

GPT Actions:

```yaml
openapi: 3.0.1
info:
  title: KAYAK - Flights, Hotels, Cars
  description: A plugin that allows users to search for the best deals on flights, hotels and cars
  version: v1
servers:
  - url: https://www.kayak.com
paths:
  /sherlock/aiplugin/search/flights:
    post:
      operationId: searchFlights
      x-openai-isConsequential: false
      summary: Search flights on a flight route for certain dates
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/searchFlightsRequest"
      parameters:
        - name: format
          in: query
          required: true
          schema:
            type: string
            default: json
          description: The format of the response.
      responses:
        "200":
          description: OK
        "429":
          description: Rate limited
  /sherlock/aiplugin/search/stays:
    post:
      operationId: searchStays
      x-openai-isConsequential: false
      summary: Search stays for certain dates
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/searchStaysRequest"
      parameters:
        - name: format
          in: query
          required: true
          schema:
            type: string
            default: json
          description: The format of the response.  
      responses:
        "200":
          description: OK
        "429":
          description: Rate limited
  /sherlock/aiplugin/search/cars:
    post:
      operationId: searchCars
      x-openai-isConsequential: false
      summary: Search rental cars for certain dates
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/searchCarsRequest"
      parameters:
        - name: format
          in: query
          required: true
          schema:
            type: string
            default: json
          description: The format of the response.
      responses:
        "200":
          description: OK
        "429":
          description: Rate limited
  /sherlock/aiplugin/explore:
    post:
      operationId: explore
      x-openai-isConsequential: false
      summary: Find places to go on a budget. This endpoint will return destinations that can be reached by plane within the
        given budget.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/exploreRequest"
      parameters:
        - name: format
          in: query
          required: true
          schema:
            type: string
            default: json
          description: The format of the response.
      responses:
        "200":
          description: OK
        "429":
          description: Rate limited
  /sherlock/aiplugin/insights/flights:
    post:
      operationId: flightInsights
      x-openai-isConsequential: false
      summary: This endpoint can be used when the flight route is known yet the travel dates are flexible. For example a user
        may say they want to travel for 2 weeks whenever air fares are the lowest. Another example is that a user
        specifies a travel month without exact dates.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/flightInsightsRequest"
      parameters:
        - name: format
          in: query
          required: true
          schema:
            type: string
            default: json
          description: The format of the response.
      responses:
        "200":
          description: OK
        "429":
          description: Rate limited
components:
  schemas:
    searchFlightsRequest:
      type: object
      required:
        - destination
        - departDate
      properties:
        origin:
          type: string
          description: The origin from which the flight starts. Will be approximated if not specified.
        destination:
          type: string
          description: The destination to which the flight goes
        departDate:
          type: string
          format: date
          description: Departure date of the flight at the origin
        departHourRange:
          type: array
          items:
            type: integer
          description: Range of hours in between which the outgoing flight should depart. Hours between 0 and 23, ranges such as
            [12,14]. Only needed when a specific flight departure time is requested.
        returnDate:
          type: string
          format: date
          description: Return date of the flight. Only required for round trip flights
        returnHourRange:
          type: array
          items:
            type: integer
          description: Range of hours in between which the return flight should depart. Hours between 0 and 23, ranges such as
            [12,14]. Only needed when a specific return flight departure time is requested.
        cabinClass:
          type: string
          description: Flight cabin class. Defaults to Economy class if not specified.
          enum:
            - economy
            - premium_economy
            - business
            - first
        numAdults:
          type: integer
          description: Number of adults that are flying
        numChildren:
          type: integer
          description: Number of children that are flying
        nonStopOnly:
          type: boolean
          description: Only show non-stop flights
        preferredCarriers:
          type: array
          items:
            type: string
          description: Optional list of airlines that are preferred.
        excludeCarriers:
          type: array
          items:
            type: string
          description: Optional list of airlines that should be avoided.
    searchStaysRequest:
      type: object
      required:
        - destination
        - checkinDate
        - checkoutDate
      properties:
        destination:
          type: string
          description: The city where you need a stay
        hotelName:
          type: string
          description: Name of the specific hotel for which the user wants to search. Optional only required when a specific hotel
            is requested.
        landmark:
          type: string
          description: Optional landmark to refine the location
        neighborhood:
          type: string
          description: Optional neighborhood to refine the location
        address:
          type: string
          description: Optional address to refine the location
        checkinDate:
          type: string
          format: date
          description: Check in date
        checkoutDate:
          type: string
          format: date
          description: Check out date
        numAdults:
          type: integer
          description: Number of adults that are staying.
        numChildren:
          type: integer
          description: Number of children that are staying
        numRooms:
          type: integer
          description: Number of rooms needed
        minNumStars:
          type: integer
          description: Minimum number of stars the accommodation should have
        specialRequest:
          type: string
          description: Any question or preference related to the accommodation for which we have no explicit query parameters.
        preferredAmenities:
          type: array
          items:
            $ref: "#/components/schemas/hotelAmenity"
          description: |
            Specify one or many amenities that the accommodation should offer: 
            - spa: Spa
            - pool: Pool
            - pet_friendly: Pet-friendly
            - beach_front: At the beach front
            - fitness_center: Fitness center
            - kitchen: Kitchen
            - parking: Parking
            - adult_only: Adult-only accommodation
            - wifi: Wi-Fi
            - ev_charger: Charger for electric vehicles
            - facilities_disabled_guests: Facilities for guests with disabilities
            - elevator: Elevator
        preferredFreebies:
          type: array
          items:
            $ref: "#/components/schemas/hotelFreebie"
          description: |
            Specify one or many freebies that should be included in the room rate:
            - free_cancellation: Rate includes free cancellation
            - free_breakfast: Rate includes breakfast
            - free_internet: Rate includes free Internet access
            - all_inclusive: All-inclusive rate
        preferredClassifications:
          type: array
          items:
            $ref: "#/components/schemas/hotelClassification"
          description: >
            Specify one or many classifications that allow us to understand better what kind of experience the user is
            looking for:

            - bed_and_breakfast: Bed and breakfast

            - motel: Motel

            - inn: Inn

            - capsule_hotel: Capsule hotel

            - apartment: Apartment

            - villa: Villa

            - ryokan: Ryokan

            - hostel: Hostel

            - cottage: Cottage

            - holiday_home: Holiday home
        preferredAmbiances:
          type: array
          items:
            $ref: "#/components/schemas/hotelAmbiance"
          description: >
            Specify one or many ambiances that allow us to understand better what kind of experience the user is looking
            for:

            - boutique: Boutique hotel

            - budget: Hotels that are budget-friendly

            - romantic: Hotels suited for romantic trips

            - historic: Hotels with a historic character

            - family_friendly: Family-friendly accommodations
    searchCarsRequest:
      type: object
      required:
        - origin
        - pickupDate
        - dropoffDate
      properties:
        origin:
          type: string
          description: The location where you want to pick your rental car
        destination:
          type: string
          description: The location where you want to drop off your rental car. Will take the origin if no other location is given.
        pickupDate:
          type: string
          format: date
          description: The date when you want to pick up your rental car
        pickupHour:
          type: integer
          description: Rental car pick up hour in 24-hour format. Optional parameter that defaults to noon.
        dropoffDate:
          type: string
          format: date
          description: The date when you want to drop off your rental car
        dropoffHour:
          type: integer
          description: Rental car drop off hour in 24-hour format. Optional parameter that defaults to noon.
    exploreRequest:
      type: object
      properties:
        origin:
          type: string
          description: The origin from which the flight starts. Will be approximated if not specified.
        destinationHints:
          type: array
          items:
            type: string
          description: Optional list of cities that are requested to be included in the results, if prices are available.
        departDate:
          type: string
          format: date
          description: Departure date of the flight at the origin
        returnDate:
          type: string
          format: date
          description: Return date of the flight. Must be specified when a departure date is given.
        budgetUsd:
          type: integer
          description: Expected cost of round trip flight ticket for one person
        nonStopOnly:
          type: boolean
          description: Only show non-stop flights
        useExactDates:
          type: boolean
          description: Set to true if travel on specific dates is requested. The default is flexible travel within a time period.
        minDays:
          type: integer
          description: Minimum duration that the suggested trips should have. Expressed in the number of days
        maxDays:
          type: integer
          description: Maximum duration that the suggested trips should have. Expressed in the number of days
    flightInsightsRequest:
      type: object
      required:
        - destination
        - departDate
      properties:
        origin:
          type: string
          description: The origin from which the flight starts. Will be approximated if not specified.
        destination:
          type: string
          description: The destination to which the flight goes
        departDate:
          type: string
          format: date
          description: Departure date of the flight at the origin
        returnDate:
          type: string
          format: date
          description: Return date of the flight. Only required for round trip flights
        nonStopOnly:
          type: boolean
          description: Only show non-stop pricing if non-stop flights are available on the requested route
    hotelAmenity:
      type: string
      enum:
        - spa
        - pool
        - pet_friendly
        - beach_front
        - fitness_center
        - kitchen
        - parking
        - adult_only
        - wifi
        - ev_charger
        - facilities_disabled_guests
        - elevator
    hotelFreebie:
      type: string
      enum:
        - free_cancellation
        - free_breakfast
        - free_internet
        - all_inclusive
    hotelClassification:
      type: string
      enum:
        - bed_and_breakfast
        - motel
        - inn
        - capsule_hotel
        - apartment
        - villa
        - ryokan
        - hostel
        - cottage
        - holiday_home
    hotelAmbiance:
      type: string
      enum:
        - boutique
        - budget
        - romantic
        - historic
        - family_friendly
```