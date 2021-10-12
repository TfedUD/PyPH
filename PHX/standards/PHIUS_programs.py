"""Programs take from:
- PHIUS_Multi-Family_Calculator- 021.03.23.xls
- PHIUS Guidebook, Table N-10, v3.02 | July 2021
- Honeybee ASHRAE 90.1 2019 | IECC 2021
"""

PHIUS_library = {
    "2021::PHIUS::Assembly": {
        "protocol": "PHIUS",
        "description": "Fair/Congress building",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::Courthouse::Courtroom"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Assembly",
                "identifier": "2021::PHIUS::Assembly",
                "start_hour": 13,
                "end_hour": 18,
                "annual_utilization_days": 150,
                "relative_utilization_factor": 0.5,
            },
            "loads": {
                "identifier": "2021::PHIUS::Assembly",
                "name": "2021::PHIUS::Assembly",
                "people_per_area": 0.753474,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Assembly",
                "name": "2021::PHIUS::Assembly",
                "daily_operating_hours": 5,
                "annual_utilization_days": 150,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Assembly",
                "name": "2021::PHIUS::Assembly",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_area": 12.91668,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Assembly",
                "name": "2021::PHIUS::Assembly",
                "annual_utilization_factor": 0.473153,
            },
            "loads": {
                "identifier": "2021::PHIUS::Assembly",
                "name": "2021::PHIUS::Assembly",
                "watts_per_area": 0,
            },
        },
    },
    "2021::PHIUS::Theater_Ticketing": {
        "protocol": "PHIUS",
        "description": "Booking hall",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::Retail::Entry"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Theater_Ticketing",
                "identifier": "2021::PHIUS::Theater_Ticketing",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS::Theater_Ticketing",
                "name": "2021::PHIUS::Theater_Ticketing",
                "people_per_area": 0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Theater_Ticketing",
                "name": "2021::PHIUS::Theater_Ticketing",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Theater_Ticketing",
                "name": "2021::PHIUS::Theater_Ticketing",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_area": 9.041676,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Theater_Ticketing",
                "name": "2021::PHIUS::Theater_Ticketing",
                "annual_utilization_factor": 0.519583,
            },
            "loads": {
                "identifier": "2021::PHIUS::Theater_Ticketing",
                "name": "2021::PHIUS::Theater_Ticketing",
                "watts_per_area": 0,
            },
        },
    },
    "2021::PHIUS::Canteen": {
        "protocol": "PHIUS",
        "description": "2021::PHIUS::Canteen",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::QuickServiceRestaurant::Dining"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Canteen",
                "identifier": "2021::PHIUS::Canteen",
                "start_hour": 8,
                "end_hour": 15,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Canteen",
                "name": "2021::PHIUS::Canteen",
                "people_per_area": 0.753474,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Canteen",
                "name": "2021::PHIUS::Canteen",
                "daily_operating_hours": 7,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Canteen",
                "name": "2021::PHIUS::Canteen",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_area": 6.45834,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Canteen",
                "name": "2021::PHIUS::Canteen",
                "annual_utilization_factor": 0.164583,
            },
            "loads": {
                "identifier": "2021::PHIUS::Canteen",
                "name": "2021::PHIUS::Canteen",
                "watts_per_area": 116.788315,
            },
        },
    },
    "2021::PHIUS::Hallway": {
        "protocol": "PHIUS",
        "description": "Traffic / Circulation Areas",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::MidriseApartment::Corridor"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Hallway",
                "identifier": "2021::PHIUS::Hallway",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.2,
            },
            "loads": {
                "identifier": "2021::PHIUS::Hallway",
                "name": "2021::PHIUS::Hallway",
                "people_per_area": 0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Hallway",
                "name": "2021::PHIUS::Hallway",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS::Hallway",
                "name": "2021::PHIUS::Hallway",
                "target_lux": 100,
                "target_lux_height": 0.0,
                "watts_per_area": 5.381955,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Hallway",
                "name": "2021::PHIUS::Hallway",
                "annual_utilization_factor": 0.245833,
            },
            "loads": {
                "identifier": "2021::PHIUS::Hallway",
                "name": "2021::PHIUS::Hallway",
                "watts_per_area": 0,
            },
        },
    },
    "2021::PHIUS::Classroom": {
        "protocol": "PHIUS",
        "description": "Classroom (school and nursery school)",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::PrimarySchool::Classroom"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Classroom",
                "identifier": "2021::PHIUS::Classroom",
                "start_hour": 8,
                "end_hour": 15,
                "annual_utilization_days": 200,
                "relative_utilization_factor": 0.75,
            },
            "loads": {
                "identifier": "2021::PHIUS::Classroom",
                "name": "2021::PHIUS::Classroom",
                "people_per_area": 0.269098,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Classroom",
                "name": "2021::PHIUS::Classroom",
                "daily_operating_hours": 7,
                "annual_utilization_days": 200,
                "relative_utilization_factor": 0.9,
            },
            "loads": {
                "identifier": "2021::PHIUS::Classroom",
                "name": "2021::PHIUS::Classroom",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_area": 7.642369,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Classroom",
                "name": "2021::PHIUS::Classroom",
                "annual_utilization_factor": 0.442427,
            },
            "loads": {
                "identifier": "2021::PHIUS::Classroom",
                "name": "2021::PHIUS::Classroom",
                "watts_per_area": 14.999495,
            },
        },
    },
    "2021::PHIUS::Garage_Private": {
        "protocol": "PHIUS",
        "description": "Garage buildings for offices and private use",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::Courthouse::Parking"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Garage_Private",
                "identifier": "2021::PHIUS::Garage_Private",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.05,
            },
            "loads": {
                "identifier": "2021::PHIUS::Garage_Private",
                "name": "2021::PHIUS::Garage_Private",
                "people_per_area": 0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Garage_Private",
                "name": "2021::PHIUS::Garage_Private",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Garage_Private",
                "name": "2021::PHIUS::Garage_Private",
                "target_lux": 75,
                "target_lux_height": 0.0,
                "watts_per_area": 1.614585,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Garage_Private",
                "name": "2021::PHIUS::Garage_Private",
                "annual_utilization_factor": 0.473153,
            },
            "loads": {
                "identifier": "2021::PHIUS::Garage_Private",
                "name": "2021::PHIUS::Garage_Private",
                "watts_per_area": 0,
            },
        },
    },
    "2021::PHIUS::Garage_Public": {
        "protocol": "PHIUS",
        "description": "Garage buildings for public use",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::Courthouse::Parking"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Garage_Public",
                "identifier": "2021::PHIUS::Garage_Public",
                "start_hour": 9,
                "end_hour": 24,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 0.2,
            },
            "loads": {
                "identifier": "2021::PHIUS::Garage_Public",
                "name": "2021::PHIUS::Garage_Public",
                "people_per_area": 0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Garage_Public",
                "name": "2021::PHIUS::Garage_Public",
                "daily_operating_hours": 15,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Garage_Public",
                "name": "2021::PHIUS::Garage_Public",
                "target_lux": 100,
                "target_lux_height": 0.0,
                "watts_per_area": 1.614585,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Garage_Public",
                "name": "2021::PHIUS::Garage_Public",
                "annual_utilization_factor": 0.473153,
            },
            "loads": {
                "identifier": "2021::PHIUS::Garage_Public",
                "name": "2021::PHIUS::Garage_Public",
                "watts_per_area": 0,
            },
        },
    },
    "2021::PHIUS::Gym": {
        "protocol": "PHIUS",
        "description": "Sports hall (without public viewing area)",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::SmallHotel::Exercise"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Gym",
                "identifier": "2021::PHIUS::Gym",
                "start_hour": 8,
                "end_hour": 23,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 0.7,
            },
            "loads": {
                "identifier": "2021::PHIUS::Gym",
                "name": "2021::PHIUS::Gym",
                "people_per_area": 0.214632,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Gym",
                "name": "2021::PHIUS::Gym",
                "daily_operating_hours": 15,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Gym",
                "name": "2021::PHIUS::Gym",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_area": 9.68751,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Gym",
                "name": "2021::PHIUS::Gym",
                "annual_utilization_factor": 0.4375,
            },
            "loads": {
                "identifier": "2021::PHIUS::Gym",
                "name": "2021::PHIUS::Gym",
                "watts_per_area": 18.621547,
            },
        },
    },
    "2021::PHIUS::Hospital_Ward": {
        "protocol": "PHIUS",
        "description": "Hospital ward or dormitory",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::Hospital::PatRoom"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Hospital_Ward",
                "identifier": "2021::PHIUS::Hospital_Ward",
                "start_hour": 8,
                "end_hour": 15,
                "annual_utilization_days": 200,
                "relative_utilization_factor": 0.75,
            },
            "loads": {
                "identifier": "2021::PHIUS::Hospital_Ward",
                "name": "2021::PHIUS::Hospital_Ward",
                "people_per_area": 0.05382,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Hospital_Ward",
                "name": "2021::PHIUS::Hospital_Ward",
                "daily_operating_hours": 7,
                "annual_utilization_days": 200,
                "relative_utilization_factor": 0.5,
            },
            "loads": {
                "identifier": "2021::PHIUS::Hospital_Ward",
                "name": "2021::PHIUS::Hospital_Ward",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_area": 7.319452,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Hospital_Ward",
                "name": "2021::PHIUS::Hospital_Ward",
                "annual_utilization_factor": 0.594292,
            },
            "loads": {
                "identifier": "2021::PHIUS::Hospital_Ward",
                "name": "2021::PHIUS::Hospital_Ward",
                "watts_per_area": 21.5278,
            },
        },
    },
    "2021::PHIUS::Hotel_Bedroom": {
        "protocol": "PHIUS",
        "description": "Hotel bedroom",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::LargeHotel::GuestRoom"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Hotel_Bedroom",
                "identifier": "2021::PHIUS::Hotel_Bedroom",
                "start_hour": 21,
                "end_hour": 8,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 0.25,
            },
            "loads": {
                "identifier": "2021::PHIUS::Hotel_Bedroom",
                "name": "2021::PHIUS::Hotel_Bedroom",
                "people_per_area": 0.038427,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Hotel_Bedroom",
                "name": "2021::PHIUS::Hotel_Bedroom",
                "daily_operating_hours": 11,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 0.3,
            },
            "loads": {
                "identifier": "2021::PHIUS::Hotel_Bedroom",
                "name": "2021::PHIUS::Hotel_Bedroom",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_area": 4.413199,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Hotel_Bedroom",
                "name": "2021::PHIUS::Hotel_Bedroom",
                "annual_utilization_factor": 0.315303,
            },
            "loads": {
                "identifier": "2021::PHIUS::Hotel_Bedroom",
                "name": "2021::PHIUS::Hotel_Bedroom",
                "watts_per_area": 6.748965,
            },
        },
    },
    "2021::PHIUS::Kitchen_Commercial_Cooking": {
        "protocol": "PHIUS",
        "description": "Kitchen in non-residential buildings",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::FullServiceRestaurant::Kitchen"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Kitchen_Commercial_Cooking",
                "identifier": "2021::PHIUS::Kitchen_Commercial_Cooking",
                "start_hour": 10,
                "end_hour": 23,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Kitchen_Commercial_Cooking",
                "name": "2021::PHIUS::Kitchen_Commercial_Cooking",
                "people_per_area": 0.05382,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Kitchen_Commercial_Cooking",
                "name": "2021::PHIUS::Kitchen_Commercial_Cooking",
                "daily_operating_hours": 13,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Kitchen_Commercial_Cooking",
                "name": "2021::PHIUS::Kitchen_Commercial_Cooking",
                "target_lux": 500,
                "target_lux_height": 0.8,
                "watts_per_area": 11.732651,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Kitchen_Commercial_Cooking",
                "name": "2021::PHIUS::Kitchen_Commercial_Cooking",
                "annual_utilization_factor": 0.164583,
            },
            "loads": {
                "identifier": "2021::PHIUS::Kitchen_Commercial_Cooking",
                "name": "2021::PHIUS::Kitchen_Commercial_Cooking",
                "watts_per_area": 403.969167,
            },
        },
    },
    "2021::PHIUS::Kitchen_Commercial_Prep_Room": {
        "protocol": "PHIUS",
        "description": "Kitchen preparation room or storeroom",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::SuperMarket::Deli"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Kitchen_Commercial_Prep_Room",
                "identifier": "2021::PHIUS::Kitchen_Commercial_Prep_Room",
                "start_hour": 7,
                "end_hour": 23,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 0.5,
            },
            "loads": {
                "identifier": "2021::PHIUS::Kitchen_Commercial_Prep_Room",
                "name": "2021::PHIUS::Kitchen_Commercial_Prep_Room",
                "people_per_area": 0.086111,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Kitchen_Commercial_Prep_Room",
                "name": "2021::PHIUS::Kitchen_Commercial_Prep_Room",
                "daily_operating_hours": 16,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Kitchen_Commercial_Prep_Room",
                "name": "2021::PHIUS::Kitchen_Commercial_Prep_Room",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_area": 11.732651,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Kitchen_Commercial_Prep_Room",
                "name": "2021::PHIUS::Kitchen_Commercial_Prep_Room",
                "annual_utilization_factor": 0.606735,
            },
            "loads": {
                "identifier": "2021::PHIUS::Kitchen_Commercial_Prep_Room",
                "name": "2021::PHIUS::Kitchen_Commercial_Prep_Room",
                "watts_per_area": 8.934037,
            },
        },
    },
    "2021::PHIUS::Laundry_Public": {
        "protocol": "PHIUS",
        "description": "Common Laundry",
        "source": ["MF_Calculator_2021", "2019::LargeHotel::Laundry"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Laundry_Public",
                "identifier": "2021::PHIUS::Laundry_Public",
                "start_hour": 0,
                "end_hour": 24,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Laundry_Public",
                "name": "2021::PHIUS::Laundry_Public",
                "people_per_area": 0.107639,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Laundry_Public",
                "name": "2021::PHIUS::Laundry_Public",
                "daily_operating_hours": 24,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Laundry_Public",
                "name": "2021::PHIUS::Laundry_Public",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_area": 5.704867,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Laundry_Public",
                "name": "2021::PHIUS::Laundry_Public",
                "annual_utilization_factor": 0.447888,
            },
            "loads": {
                "identifier": "2021::PHIUS::Laundry_Public",
                "name": "2021::PHIUS::Laundry_Public",
                "watts_per_area": 61.677147,
            },
        },
    },
    "2021::PHIUS::Library_Reading_Room": {
        "protocol": "PHIUS",
        "description": "Library - reading rooms",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::SecondarySchool::Library"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Library_Reading_Room",
                "identifier": "2021::PHIUS::Library_Reading_Room",
                "start_hour": 8,
                "end_hour": 20,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS::Library_Reading_Room",
                "name": "2021::PHIUS::Library_Reading_Room",
                "people_per_area": 0.107639,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Library_Reading_Room",
                "name": "2021::PHIUS::Library_Reading_Room",
                "daily_operating_hours": 12,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS::Library_Reading_Room",
                "name": "2021::PHIUS::Library_Reading_Room",
                "target_lux": 500,
                "target_lux_height": 0.8,
                "watts_per_area": 8.934037,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Library_Reading_Room",
                "name": "2021::PHIUS::Library_Reading_Room",
                "annual_utilization_factor": 0.462476,
            },
            "loads": {
                "identifier": "2021::PHIUS::Library_Reading_Room",
                "name": "2021::PHIUS::Library_Reading_Room",
                "watts_per_area": 10.010427,
            },
        },
    },
    "2021::PHIUS::Library_Storage": {
        "protocol": "PHIUS",
        "description": "Library magazine and stores",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", ""],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Library_Storage",
                "identifier": "2021::PHIUS::Library_Storage",
                "start_hour": 8,
                "end_hour": 20,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 0.1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Library_Storage",
                "name": "2021::PHIUS::Library_Storage",
                "people_per_area": 0.107639,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Library_Storage",
                "name": "2021::PHIUS::Library_Storage",
                "daily_operating_hours": 12,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Library_Storage",
                "name": "2021::PHIUS::Library_Storage",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_area": 8.934037,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Library_Storage",
                "name": "2021::PHIUS::Library_Storage",
                "annual_utilization_factor": 0.462476,
            },
            "loads": {
                "identifier": "2021::PHIUS::Library_Storage",
                "name": "2021::PHIUS::Library_Storage",
                "watts_per_area": 10.010427,
            },
        },
    },
    "2021::PHIUS::Library_Stacks": {
        "protocol": "PHIUS",
        "description": "Library-open stacks areas",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", ""],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Library_Stacks",
                "identifier": "2021::PHIUS::Library_Stacks",
                "start_hour": 8,
                "end_hour": 20,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Library_Stacks",
                "name": "2021::PHIUS::Library_Stacks",
                "people_per_area": 0.107639,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Library_Stacks",
                "name": "2021::PHIUS::Library_Stacks",
                "daily_operating_hours": 12,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Library_Stacks",
                "name": "2021::PHIUS::Library_Stacks",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_area": 8.934037,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Library_Stacks",
                "name": "2021::PHIUS::Library_Stacks",
                "annual_utilization_factor": 0.462476,
            },
            "loads": {
                "identifier": "2021::PHIUS::Library_Stacks",
                "name": "2021::PHIUS::Library_Stacks",
                "watts_per_area": 10.010427,
            },
        },
    },
    "2021::PHIUS::Museum_Exhibition": {
        "protocol": "PHIUS",
        "description": "Exhibition rooms and museums with conservation requirements",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::Retail::Retail"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Museum_Exhibition",
                "identifier": "2021::PHIUS::Museum_Exhibition",
                "start_hour": 10,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Museum_Exhibition",
                "name": "2021::PHIUS::Museum_Exhibition",
                "people_per_area": 0.161459,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Museum_Exhibition",
                "name": "2021::PHIUS::Museum_Exhibition",
                "daily_operating_hours": 8,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Museum_Exhibition",
                "name": "2021::PHIUS::Museum_Exhibition",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_area": 11.302095,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Museum_Exhibition",
                "name": "2021::PHIUS::Museum_Exhibition",
                "annual_utilization_factor": 0.519583,
            },
            "loads": {
                "identifier": "2021::PHIUS::Museum_Exhibition",
                "name": "2021::PHIUS::Museum_Exhibition",
                "watts_per_area": 3.22917,
            },
        },
    },
    "2021::PHIUS::Server_Room": {
        "protocol": "PHIUS",
        "description": "Server room, computer center",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::MediumOffice::Elec/MechRoom"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Server_Room",
                "identifier": "2021::PHIUS::Server_Room",
                "start_hour": 0,
                "end_hour": 24,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 0.5,
            },
            "loads": {
                "identifier": "2021::PHIUS::Server_Room",
                "name": "2021::PHIUS::Server_Room",
                "people_per_area": 0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Server_Room",
                "name": "2021::PHIUS::Server_Room",
                "daily_operating_hours": 24,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 0.5,
            },
            "loads": {
                "identifier": "2021::PHIUS::Server_Room",
                "name": "2021::PHIUS::Server_Room",
                "target_lux": 500,
                "target_lux_height": 0.8,
                "watts_per_area": 4.628477,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Server_Room",
                "name": "2021::PHIUS::Server_Room",
                "annual_utilization_factor": 0.467636,
            },
            "loads": {
                "identifier": "2021::PHIUS::Server_Room",
                "name": "2021::PHIUS::Server_Room",
                "watts_per_area": 2.906253,
            },
        },
    },
    "2021::PHIUS::Manufacturing_Workshop": {
        "protocol": "PHIUS",
        "description": "Workshop, assembly,manufacturing",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::Laboratory::Open lab"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Manufacturing_Workshop",
                "identifier": "2021::PHIUS::Manufacturing_Workshop",
                "start_hour": 7,
                "end_hour": 16,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS::Manufacturing_Workshop",
                "name": "2021::PHIUS::Manufacturing_Workshop",
                "people_per_area": 0.05382,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Manufacturing_Workshop",
                "name": "2021::PHIUS::Manufacturing_Workshop",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS::Manufacturing_Workshop",
                "name": "2021::PHIUS::Manufacturing_Workshop",
                "target_lux": 500,
                "target_lux_height": 0.8,
                "watts_per_area": 14.315987,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Manufacturing_Workshop",
                "name": "2021::PHIUS::Manufacturing_Workshop",
                "annual_utilization_factor": 0.307021,
            },
            "loads": {
                "identifier": "2021::PHIUS::Manufacturing_Workshop",
                "name": "2021::PHIUS::Manufacturing_Workshop",
                "watts_per_area": 43.0556,
            },
        },
    },
    "2021::PHIUS::Office_Meeting_Room": {
        "protocol": "PHIUS",
        "description": "Meeting conference and seminar room",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::LargeOffice::Conference"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Office_Meeting_Room",
                "identifier": "2021::PHIUS::Office_Meeting_Room",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.5,
            },
            "loads": {
                "identifier": "2021::PHIUS::Office_Meeting_Room",
                "name": "2021::PHIUS::Office_Meeting_Room",
                "people_per_area": 0.538196,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Office_Meeting_Room",
                "name": "2021::PHIUS::Office_Meeting_Room",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Office_Meeting_Room",
                "name": "2021::PHIUS::Office_Meeting_Room",
                "target_lux": 500,
                "target_lux_height": 0.8,
                "watts_per_area": 10.440983,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Office_Meeting_Room",
                "name": "2021::PHIUS::Office_Meeting_Room",
                "annual_utilization_factor": 0.512215,
            },
            "loads": {
                "identifier": "2021::PHIUS::Office_Meeting_Room",
                "name": "2021::PHIUS::Office_Meeting_Room",
                "watts_per_area": 3.982643,
            },
        },
    },
    "2021::PHIUS::Office_Workspace_Open": {
        "protocol": "PHIUS",
        "description": "Landscaped office (seven or more workplaces)",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::LargeOffice::OpenOffice"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Office_Workspace_Open",
                "identifier": "2021::PHIUS::Office_Workspace_Open",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS::Office_Workspace_Open",
                "name": "2021::PHIUS::Office_Workspace_Open",
                "people_per_area": 0.056511,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Office_Workspace_Open",
                "name": "2021::PHIUS::Office_Workspace_Open",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS::Office_Workspace_Open",
                "name": "2021::PHIUS::Office_Workspace_Open",
                "target_lux": 500,
                "target_lux_height": 0.8,
                "watts_per_area": 6.565979,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Office_Workspace_Open",
                "name": "2021::PHIUS::Office_Workspace_Open",
                "annual_utilization_factor": 0.512215,
            },
            "loads": {
                "identifier": "2021::PHIUS::Office_Workspace_Open",
                "name": "2021::PHIUS::Office_Workspace_Open",
                "watts_per_area": 7.642369,
            },
        },
    },
    "2021::PHIUS::Office_Workspace_Semiopen": {
        "protocol": "PHIUS",
        "description": "Workgroup Office (2-6 workplaces)",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::LargeOffice::ClosedOffice"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Office_Workspace_Semiopen",
                "identifier": "2021::PHIUS::Office_Workspace_Semiopen",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.7,
            },
            "loads": {
                "identifier": "2021::PHIUS::Office_Workspace_Semiopen",
                "name": "2021::PHIUS::Office_Workspace_Semiopen",
                "people_per_area": 0.051129,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Office_Workspace_Semiopen",
                "name": "2021::PHIUS::Office_Workspace_Semiopen",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.7,
            },
            "loads": {
                "identifier": "2021::PHIUS::Office_Workspace_Semiopen",
                "name": "2021::PHIUS::Office_Workspace_Semiopen",
                "target_lux": 500,
                "target_lux_height": 0.8,
                "watts_per_area": 7.965286,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Office_Workspace_Semiopen",
                "name": "2021::PHIUS::Office_Workspace_Semiopen",
                "annual_utilization_factor": 0.512215,
            },
            "loads": {
                "identifier": "2021::PHIUS::Office_Workspace_Semiopen",
                "name": "2021::PHIUS::Office_Workspace_Semiopen",
                "watts_per_area": 6.888896,
            },
        },
    },
    "2021::PHIUS::Office_Workspace_Closed": {
        "protocol": "PHIUS",
        "description": "Personal office (single occupant)",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", ""],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Office_Workspace_Closed",
                "identifier": "2021::PHIUS::Office_Workspace_Closed",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.7,
            },
            "loads": {
                "identifier": "2021::PHIUS::Office_Workspace_Closed",
                "name": "2021::PHIUS::Office_Workspace_Closed",
                "people_per_area": 0.051129,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Office_Workspace_Closed",
                "name": "2021::PHIUS::Office_Workspace_Closed",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.7,
            },
            "loads": {
                "identifier": "2021::PHIUS::Office_Workspace_Closed",
                "name": "2021::PHIUS::Office_Workspace_Closed",
                "target_lux": 500,
                "target_lux_height": 0.8,
                "watts_per_area": 7.965286,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Office_Workspace_Closed",
                "name": "2021::PHIUS::Office_Workspace_Closed",
                "annual_utilization_factor": 0.512215,
            },
            "loads": {
                "identifier": "2021::PHIUS::Office_Workspace_Closed",
                "name": "2021::PHIUS::Office_Workspace_Closed",
                "watts_per_area": 6.888896,
            },
        },
    },
    "2021::PHIUS::Other_Habitable": {
        "protocol": "PHIUS",
        "description": "Other Habitable Room",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::LargeOffice::OpenOffice"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Other_Habitable",
                "identifier": "2021::PHIUS::Other_Habitable",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.5,
            },
            "loads": {
                "identifier": "2021::PHIUS::Other_Habitable",
                "name": "2021::PHIUS::Other_Habitable",
                "people_per_area": 0.056511,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Other_Habitable",
                "name": "2021::PHIUS::Other_Habitable",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Other_Habitable",
                "name": "2021::PHIUS::Other_Habitable",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_area": 6.565979,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Other_Habitable",
                "name": "2021::PHIUS::Other_Habitable",
                "annual_utilization_factor": 0.512215,
            },
            "loads": {
                "identifier": "2021::PHIUS::Other_Habitable",
                "name": "2021::PHIUS::Other_Habitable",
                "watts_per_area": 7.642369,
            },
        },
    },
    "2021::PHIUS::Other_Non_Habitable": {
        "protocol": "PHIUS",
        "description": "Auxiliary spaces without habitable rooms",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::LargeOffice::Storage"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Other_Non_Habitable",
                "identifier": "2021::PHIUS::Other_Non_Habitable",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Other_Non_Habitable",
                "name": "2021::PHIUS::Other_Non_Habitable",
                "people_per_area": 0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Other_Non_Habitable",
                "name": "2021::PHIUS::Other_Non_Habitable",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Other_Non_Habitable",
                "name": "2021::PHIUS::Other_Non_Habitable",
                "target_lux": 100,
                "target_lux_height": 0.8,
                "watts_per_area": 4.090282,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Other_Non_Habitable",
                "name": "2021::PHIUS::Other_Non_Habitable",
                "annual_utilization_factor": 0.512215,
            },
            "loads": {
                "identifier": "2021::PHIUS::Other_Non_Habitable",
                "name": "2021::PHIUS::Other_Non_Habitable",
                "watts_per_area": 0,
            },
        },
    },
    "2021::PHIUS::Restaurant": {
        "protocol": "PHIUS",
        "description": "2021::PHIUS::Restaurant",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::FullServiceRestaurant::Dining"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Restaurant",
                "identifier": "2021::PHIUS::Restaurant",
                "start_hour": 10,
                "end_hour": 24,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Restaurant",
                "name": "2021::PHIUS::Restaurant",
                "people_per_area": 0.753474,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Restaurant",
                "name": "2021::PHIUS::Restaurant",
                "daily_operating_hours": 14,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Restaurant",
                "name": "2021::PHIUS::Restaurant",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_area": 6.45834,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Restaurant",
                "name": "2021::PHIUS::Restaurant",
                "annual_utilization_factor": 0.164583,
            },
            "loads": {
                "identifier": "2021::PHIUS::Restaurant",
                "name": "2021::PHIUS::Restaurant",
                "watts_per_area": 64.927845,
            },
        },
    },
    "2021::PHIUS::Restroom_Public": {
        "protocol": "PHIUS",
        "description": "Toilets and sanitary facilities in non residential buildings",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::MediumOffice::Restroom"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Restroom_Public",
                "identifier": "2021::PHIUS::Restroom_Public",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Restroom_Public",
                "name": "2021::PHIUS::Restroom_Public",
                "people_per_area": 0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Restroom_Public",
                "name": "2021::PHIUS::Restroom_Public",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Restroom_Public",
                "name": "2021::PHIUS::Restroom_Public",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_area": 6.781257,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Restroom_Public",
                "name": "2021::PHIUS::Restroom_Public",
                "annual_utilization_factor": 0.467636,
            },
            "loads": {
                "identifier": "2021::PHIUS::Restroom_Public",
                "name": "2021::PHIUS::Restroom_Public",
                "watts_per_area": 2.906253,
            },
        },
    },
    "2021::PHIUS::Department_Store": {
        "protocol": "PHIUS",
        "description": "Retail shop/Department store",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::Retail::Core_Retail"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Department_Store",
                "identifier": "2021::PHIUS::Department_Store",
                "start_hour": 8,
                "end_hour": 20,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Department_Store",
                "name": "2021::PHIUS::Department_Store",
                "people_per_area": 0.161459,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Department_Store",
                "name": "2021::PHIUS::Department_Store",
                "daily_operating_hours": 12,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Department_Store",
                "name": "2021::PHIUS::Department_Store",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_area": 11.302095,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Department_Store",
                "name": "2021::PHIUS::Department_Store",
                "annual_utilization_factor": 0.519583,
            },
            "loads": {
                "identifier": "2021::PHIUS::Department_Store",
                "name": "2021::PHIUS::Department_Store",
                "watts_per_area": 3.22917,
            },
        },
    },
    "2021::PHIUS::Grocery": {
        "description": "Retail shop/department store (food department with refrigerated products)",
        "protocol": "PHIUS",
        "description": "",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::SuperMarket::Sales"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Grocery",
                "identifier": "2021::PHIUS::Grocery",
                "start_hour": 8,
                "end_hour": 20,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Grocery",
                "name": "2021::PHIUS::Grocery",
                "people_per_area": 0.086111,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Grocery",
                "name": "2021::PHIUS::Grocery",
                "daily_operating_hours": 12,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Grocery",
                "name": "2021::PHIUS::Grocery",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_area": 11.302095,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Grocery",
                "name": "2021::PHIUS::Grocery",
                "annual_utilization_factor": 0.606735,
            },
            "loads": {
                "identifier": "2021::PHIUS::Grocery",
                "name": "2021::PHIUS::Grocery",
                "watts_per_area": 10.979178,
            },
        },
    },
    "2021::PHIUS::Storage_Archive": {
        "protocol": "PHIUS",
        "description": "Storeroom technical equipment room or archive",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::Warehouse::Fine"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Storage_Archive",
                "identifier": "2021::PHIUS::Storage_Archive",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.02,
            },
            "loads": {
                "identifier": "2021::PHIUS::Storage_Archive",
                "name": "2021::PHIUS::Storage_Archive",
                "people_per_area": 0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Storage_Archive",
                "name": "2021::PHIUS::Storage_Archive",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Storage_Archive",
                "name": "2021::PHIUS::Storage_Archive",
                "target_lux": 100,
                "target_lux_height": 0.8,
                "watts_per_area": 7.427091,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Storage_Archive",
                "name": "2021::PHIUS::Storage_Archive",
                "annual_utilization_factor": 0.427397,
            },
            "loads": {
                "identifier": "2021::PHIUS::Storage_Archive",
                "name": "2021::PHIUS::Storage_Archive",
                "watts_per_area": 0,
            },
        },
    },
    "2021::PHIUS::School_Auditorium": {
        "protocol": "PHIUS",
        "description": "Lecture room, auditorium",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::SecondarySchool::Auditorium"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::School_Auditorium",
                "identifier": "2021::PHIUS::School_Auditorium",
                "start_hour": 8,
                "end_hour": 18,
                "annual_utilization_days": 150,
                "relative_utilization_factor": 0.75,
            },
            "loads": {
                "identifier": "2021::PHIUS::School_Auditorium",
                "name": "2021::PHIUS::School_Auditorium",
                "people_per_area": 1.614587,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::School_Auditorium",
                "name": "2021::PHIUS::School_Auditorium",
                "daily_operating_hours": 12,
                "annual_utilization_days": 150,
                "relative_utilization_factor": 0.7,
            },
            "loads": {
                "identifier": "2021::PHIUS::School_Auditorium",
                "name": "2021::PHIUS::School_Auditorium",
                "target_lux": 500,
                "target_lux_height": 0.8,
                "watts_per_area": 6.565979,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::School_Auditorium",
                "name": "2021::PHIUS::School_Auditorium",
                "annual_utilization_factor": 0.462476,
            },
            "loads": {
                "identifier": "2021::PHIUS::School_Auditorium",
                "name": "2021::PHIUS::School_Auditorium",
                "watts_per_area": 4.951394,
            },
        },
    },
    "2021::PHIUS::Theater_Seating": {
        "protocol": "PHIUS",
        "description": "Spectators and audience area of theaters and event locations",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::Courthouse::Courtroom"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Theater_Seating",
                "identifier": "2021::PHIUS::Theater_Seating",
                "start_hour": 19,
                "end_hour": 23,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Theater_Seating",
                "name": "2021::PHIUS::Theater_Seating",
                "people_per_area": 0.753474,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Theater_Seating",
                "name": "2021::PHIUS::Theater_Seating",
                "daily_operating_hours": 4,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Theater_Seating",
                "name": "2021::PHIUS::Theater_Seating",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_area": 12.91668,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Theater_Seating",
                "name": "2021::PHIUS::Theater_Seating",
                "annual_utilization_factor": 0.473153,
            },
            "loads": {
                "identifier": "2021::PHIUS::Theater_Seating",
                "name": "2021::PHIUS::Theater_Seating",
                "watts_per_area": 0,
            },
        },
    },
    "2021::PHIUS::Theater_Lobby": {
        "protocol": "PHIUS",
        "description": "Foyer (theaters and event locations)",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::MediumOffice::Lobby"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Theater_Lobby",
                "identifier": "2021::PHIUS::Theater_Lobby",
                "start_hour": 19,
                "end_hour": 23,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.5,
            },
            "loads": {
                "identifier": "2021::PHIUS::Theater_Lobby",
                "name": "2021::PHIUS::Theater_Lobby",
                "people_per_area": 0.107639,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Theater_Lobby",
                "name": "2021::PHIUS::Theater_Lobby",
                "daily_operating_hours": 4,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "2021::PHIUS::Theater_Lobby",
                "name": "2021::PHIUS::Theater_Lobby",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_area": 9.041676,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Theater_Lobby",
                "name": "2021::PHIUS::Theater_Lobby",
                "annual_utilization_factor": 0.467636,
            },
            "loads": {
                "identifier": "2021::PHIUS::Theater_Lobby",
                "name": "2021::PHIUS::Theater_Lobby",
                "watts_per_area": 2.906253,
            },
        },
    },
    "2021::PHIUS::Theater_Stage": {
        "protocol": "PHIUS",
        "description": "Stage (theaters and event locations)",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::MediumOffice::OpenOffice"],
        "people": {
            "schedule": {
                "name": "2021::PHIUS::Theater_Stage",
                "identifier": "2021::PHIUS::Theater_Stage",
                "start_hour": 13,
                "end_hour": 23,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "2021::PHIUS::Theater_Stage",
                "name": "2021::PHIUS::Theater_Stage",
                "people_per_area": 0.056511,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "2021::PHIUS::Theater_Stage",
                "name": "2021::PHIUS::Theater_Stage",
                "daily_operating_hours": 10,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.6,
            },
            "loads": {
                "identifier": "2021::PHIUS::Theater_Stage",
                "name": "2021::PHIUS::Theater_Stage",
                "target_lux": 1000,
                "target_lux_height": 0.8,
                "watts_per_area": 6.565979,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "2021::PHIUS::Theater_Stage",
                "name": "2021::PHIUS::Theater_Stage",
                "annual_utilization_factor": 0.467636,
            },
            "loads": {
                "identifier": "2021::PHIUS::Theater_Stage",
                "name": "2021::PHIUS::Theater_Stage",
                "watts_per_area": 10.333344,
            },
        },
    },
}
