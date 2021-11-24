![Velomatch](resources/velomatch.png)

# Stock Broker

The Velomatch stock broker enables retailers to provide semi-real time updates for stock levels within their distribution warehouses or dealer shops. This readme details the technical details and requirements of developing and integrating with our stock broker service. By integrating stock within the solution, Velomatch is able to: 

- Indicate stock availability to all prospective clients
- Drive high quality enquires for bikes in stock

## Data Required

**Top Level** - These properties are used to identify and authenticate the information being sent. Note, the password should never be sent over as plain text and all of the information sent should always be encrypted. See the security section of this document for more information. 

| Property   | Type   | Description                                                                                        |
|------------|--------|----------------------------------------------------------------------------------------------------|
| username   | string | The user name assigned to the end point being used for integration.                                |
| password   | string | The password assigned to the end point being used for integration.                                 |  
| datetime   | string | The date and time in ISO 8601 format representing when the data was accurate.                      |
| facilities | object | An object object representing a group of storage facilities in which data is going to be sent for. |

**Facilities** - A facility represents a shop floor, store, warehouse or distribution centre where stock is held ready for purchase. 

| Property     | Type    | Description                                                                                        |
|--------------|---------|----------------------------------------------------------------------------------------------------|
| facility     | object  | An object representing a facility where stock is stored and available for purchase.                |
| facilitycode | string  | The code given to identify the facility in which stock shall be provided.                          |
| partial      | boolean | Indicate if the update given for the facility is a complete inventory of stock (```false```), or a partial update (```true```). If a complete inventory is provided, any products not specified shall have an assumed a stock value of zero. |
| stock        | object  | An object representing a list of items which are in stock.                                         |
| forecast     | object  | An object representing a list of items for which a delivery is forecasted.                         |

**Forecast** - A forecast object represents a forecasted delivery of new stock which shall be available for purchase. All forecasts should be sent for a facility with each update and any previously sent forecasts which are not sent again shall be assumed cancelled. 

| Property     | Type    | Description                                                                                                  |
|--------------|---------|--------------------------------------------------------------------------------------------------------------|
| forecast     | object  | An object representing a forecasted delivery of stock to the facility.                                       |
| forecastid   | string  | A unique identifier for the forecast delivery within in the scope of the facility.                            |
| datetime     | string  | The date and time in ISO 8601 format representing when new stock is forecasted to be available for purchase. |
| stock        | Number  | An object representing a list of items which will be delivered.                                              |


**Stock** - A generic object representing stock and the quality available. Note, this object is used in both the facility and forecast objects, and as such either represents the live stock position, or the products which are forecasted to be delivered. 

| Property     | Type    | Description                                                                                                 |
|--------------|---------|-------------------------------------------------------------------------------------------------------------|
| unit         | object  | An object representing a unit of stock                                                                      |
| sku          | string  | The stock keeping unit code given to identify the stock item.                                               |
| quantity     | Number  | The quantity of units available for sale, or to be delivered to this facility (depending on parent object). |


## Data Format

The business supports representing the data specified in one of three formats. JSON, XML and Microsoft Excel. 

### JSON

JSON (JavaScript Object Notation) is an open standard file format and data interchange format that uses human-readable text to store and transmit data objects consisting of attribute–value pairs and arrays (or other serializable values).  It is a common data format with diverse uses in electronic data interchange, including that of web applications with servers. JSON is a language-independent data format. It was derived from JavaScript, but many modern programming languages include code to generate and parse JSON-format data. JSON filenames use the extension .json. All properties are required unless specified. 

**Top Level** - An example of the json for this is shown below. 

```json
{
  "username": "DistributerFoo",  
  "password": "PasswordBar",
  "datetime": "2021-11-24T14:40:40+0000", // ISO 8601
  "facilities": { ... }, // See Facilities below
}
```

**Facilities** - An example of the json for this is shown below. 

```json
"facility": [
    {
        "facilitycode": "f001",  
        "partial": false,
        "stock": { ... }, // See stock below
        "forecast": { ... }, // See forecast below
    },
    {
        "facilitycode": "f002",  
        "partial": true,
        "stock": { ... }, // See stock below
        "forecast": { ... }, // See forecast below
    },
]
```

**Forecast** - An example of the json for this is shown below. 

```json
"forecast": [
    {
        "forecastid": "f1001",
        "datetime": "2021-11-25T14:40:40+0000", // ISO 8601
        "stock": { ... }, // See stock below
    }
    {
        "forecastid": "f1002",
        "datetime": "2021-11-26T14:40:40+0000", // ISO 8601
        "stock": { ... }, // See stock below
    }
]
```

**Stock** - An example of the json for this is shown below. 

```json
"unit": [
    {
        "sku": "123-456-789",
        "quantity": 4,
    },
    {
        "sku": "223-456-789",
        "quantity": 7,
    },
    {
        "sku": "324-456-789",
        "quantity": 0,
    },
]
```

**Complete Example** - Below is a fictional representation of a single JSON file updating the stock of two facilities with deliveries forecasted. 

```json
{
    "username": "DistributerFoo",
    "password": "PasswordBar",
    "datetime": "2021-11-24T14:40:40+0000",
    "facility": [
        {
            "facilitycode": "f001",
            "partial": false,
            "stock": { 
                "unit": [
                    {
                        "sku": "123-456-789",
                        "quantity": 4,
                    },
                    {
                        "sku": "223-456-789",
                        "quantity": 7,
                    },
                    {
                        "sku": "324-456-789",
                        "quantity": 0,
                    },
                ]
             },
            "forecast": { 
                "forecastid": "f1001",
                "datetime": "2021-11-26T14:40:40+0000",
                "stock": { 
                    "unit": [
                        {
                            "sku": "324-456-789",
                            "quantity": 3,
                        },
                    ]
                },
            }, 
        },
        {
            "facilitycode": "f002", 
            "partial": true,
            "stock": { 
                "unit": [
                    {
                        "sku": "423-456-789",
                        "quantity": 3,
                    },
                    {
                        "sku": "523-456-789",
                        "quantity": 6,
                    },
                    {
                        "sku": "624-456-789",
                        "quantity": 2,
                    },
                ]
             },
            "forecast": [ 
                { 
                    "forecastid": "f1002",
                    "datetime": "2021-11-28T14:40:40+0000",
                    "stock": { 
                        "unit": [
                            {
                                "sku": "624-456-789",
                                "quantity": 2,
                            },
                        ]
                    },
                }, 
                { 
                    "forecastid": "f1003",
                    "datetime": "2021-12-01T14:40:40+0000",
                    "stock": { 
                        "unit": [
                            {
                                "sku": "423-456-789",
                                "quantity": 1,
                            },
                            {
                                "sku": "524-456-789",
                                "quantity": 3,
                            },
                        ]
                    },
                }, 
            ]
        }
    ]
}
```

### XML

eXtensible Markup Language (XML) is a markup language that defines a set of rules for encoding documents in a format that is both human-readable and machine-readable. The World Wide Web Consortium's XML 1.0 Specification of 1998 and several other related specifications all of them free open standards—define XML. The design goals of XML emphasize simplicity, generality, and usability across the Internet. It is a textual data format with strong support via Unicode for different human languages. Although the design of XML focuses on documents, the language is widely used for the representation of arbitrary data structures such as those used in web services. Several schema systems exist to aid in the definition of XML-based languages, while programmers have developed many application programming interfaces (APIs) to aid the processing of XML data. 


**Top Level** - An example of the XML for this is shown below.

```xml
<Velomatch>
    <StockBroker username="DistributerFoo" password="PasswordBar" DateTime="2021-11-24T14:40:40+0000">
    </StockBroker>
</Velomatch>
```

**Facilities** - An example of the XML for this is shown below.

```xml
<Facilities>
    <Facility facilityCode="f001" partial="false">
    </Facility>
</Facilities>
```

**Forecast** - An example of the xml for this is shown below. 

```xml
<Forecasts>
    <Forecast forecastid="f1001" datetime="2021-11-25T14:40:40+0000">
    </Forecast>
    <Forecast forecastid="f1002" datetime="2021-11-26T14:40:40+0000">
    </Forecast>
</Forecasts>
```

**Stock** - An example of the xml for this is shown below. 

```xml
<Stock>
    <Unit sku="123-456-789" quantity="4" />
    <Unit sku="223-456-789" quantity="7" />
    <Unit sku="323-456-789" quantity="6" />
</Stock>
```

**Complete Example** - Below is a fictional representation of a single xml file updating the stock of two facilities with deliveries forecasted. 

```xml
<?xml version="1.0" encoding="ISO-8859-1" ?>
<Velomatch>
    <StockBroker username="DistributerFoo" password="PasswordBar" DateTime="2021-11-24T14:40:40+0000">
        <Facilities>
            <Facility facilityCode="f001" partial="false">
                <Stock>
                    <Unit sku="123-456-789" quantity="4" />
                    <Unit sku="223-456-789" quantity="7" />
                    <Unit sku="323-456-789" quantity="6" />
                </Stock>
                <Forecasts>
                    <Forecast forecastid="f1001" datetime="2021-11-25T14:40:40+0000">
                        <Stock>
                            <Unit sku="324-456-789" quantity="4" />
                        </Stock>
                    </Forecast>
                    <Forecast id="f1002" datetime="2021-11-26T14:40:40+0000">
                        <Stock>
                            <Unit sku="423-456-789" quantity="4" />
                            <Unit sku="523-456-789" quantity="7" />
                            <Unit sku="623-456-789" quantity="6" />
                        </Stock>
                    </Forecast>
                </Forecasts>
            </Facility>
        </Facilities>
    </StockBroker>
</Velomatch>
```

### Microsoft Excel

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## Connection 

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

### RESTfull

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

### SOAP

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

### FTP

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

### Email

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

### Web Form

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## Data Security

Velomatch takes data security very seriously and as such requires all data payloads to use asymmetric encryption. Asymmetric Encryption uses two distinct, yet related keys. One key, the Public Key, is used for encryption and the other, the Private Key, is for decryption. As implied in the name, the Private Key is intended to be private so that only the authenticated recipient can decrypt the message.

Let’s understand this with a simple asymmetric encryption example.

Pretend you’re a spy agency and you need to devise a mechanism for your agents to report in securely. You don’t need two-way communication, they have their orders, you just need regular detailed reports coming in from them. Asymmetric encryption would allow you to create public keys for the agents to encrypt their information and a private key back at headquarters that is the only way to decrypt it all. This provides an impenetrable form of one-way communication.

At the heart of Asymmetric Encryption lies a cryptographic algorithm. This algorithm uses a key generation protocol (a kind of mathematical function) to generate a key pair. Both the keys are mathematically connected with each other. This relationship between the keys differs from one algorithm to another.

The algorithm is basically a combination of two functions – encryption function and decryption function. To state the obvious, the encryption function encrypts the data and decryption function decrypts it.

When you visit any HTTPS website/webpage, your browser establishes Asymmetrically encrypted connection with that website. Your browser automatically derives the public key of the SSL/TLS certificate installed on the website (that’s why it’s called ‘Public Key’). Do you want to see what it looks like? Click the green padlock you see in front of our URL, and go to certificate details. 

Once registered as a data provider, Velomatch shares Public keys to our production environment for registered data providers. The sandbox key is however public and is available here: '''TODO'''

## Examples

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

### Python

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

### Google Colaboratory

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## Support

Velomatch is here to help and guide one through the process of achieving integration. Drop [Richard](mailto:richard@velomatch.com) a line with your problem and he will be happy to lend a hand. 

## About Velomatch

Cycling is glorious! The buying process often isn't... We're here to change that. Unbiased, expert advice without the hard sell. Make sure your next bike fits! Visit www.velomatch.com to try it out for yourself. 


