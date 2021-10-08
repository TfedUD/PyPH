"""Programs take from:
- PHIUS_Multi-Family_Calculator- 021.03.23.xls
- PHIUS Guidebook, Table N-10, v3.02 | July 2021
- Honeybee ASHRAE 90.1 2019 | IECC 2021
"""

PHIUS_library = {
    "Assembly": {
        "protocol": "PHIUS",
        "description": "Fair/Congress building",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::Courthouse::Courtroom"],
        "people": {
            "schedule": {
                "name": "Assembly",
                "identifier": "Assembly",
                "start_hour": 13,
                "end_hour": 18,
                "annual_utilization_days": 150,
                "relative_utilization_factor": 0.5,
            },
            "loads": {
                "identifier": "Assembly",
                "name": "Assembly",
                "people_per_area": 0.753474,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Assembly",
                "name": "Assembly",
                "daily_operating_hours": 5,
                "annual_utilization_days": 150,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Assembly",
                "name": "Assembly",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_area": 12.91668,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Assembly",
                "name": "Assembly",
                "annual_utilization_factor": 0.473153,
            },
            "loads": {
                "identifier": "Assembly",
                "name": "Assembly",
                "watts_per_area": 0,
            },
        },
    },
    "Theater::Ticketing": {
        "protocol": "PHIUS",
        "description": "Booking hall",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::Retail::Entry"],
        "people": {
            "schedule": {
                "name": "Theater::Ticketing",
                "identifier": "Theater::Ticketing",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "Theater::Ticketing",
                "name": "Theater::Ticketing",
                "people_per_area": 0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Theater::Ticketing",
                "name": "Theater::Ticketing",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Theater::Ticketing",
                "name": "Theater::Ticketing",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_area": 9.041676,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Theater::Ticketing",
                "name": "Theater::Ticketing",
                "annual_utilization_factor": 0.519583,
            },
            "loads": {
                "identifier": "Theater::Ticketing",
                "name": "Theater::Ticketing",
                "watts_per_area": 0,
            },
        },
    },
    "Canteen": {
        "protocol": "PHIUS",
        "description": "Canteen",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::QuickServiceRestaurant::Dining"],
        "people": {
            "schedule": {
                "name": "Canteen",
                "identifier": "Canteen",
                "start_hour": 8,
                "end_hour": 15,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Canteen",
                "name": "Canteen",
                "people_per_area": 0.753474,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Canteen",
                "name": "Canteen",
                "daily_operating_hours": 7,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Canteen",
                "name": "Canteen",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_area": 6.45834,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Canteen",
                "name": "Canteen",
                "annual_utilization_factor": 0.164583,
            },
            "loads": {
                "identifier": "Canteen",
                "name": "Canteen",
                "watts_per_area": 116.788315,
            },
        },
    },
    "Circulation::Hallway": {
        "protocol": "PHIUS",
        "description": "Traffic / Circulation Areas",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::MidriseApartment::Corridor"],
        "people": {
            "schedule": {
                "name": "Circulation::Hallway",
                "identifier": "Circulation::Hallway",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.2,
            },
            "loads": {
                "identifier": "Circulation::Hallway",
                "name": "Circulation::Hallway",
                "people_per_area": 0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Circulation::Hallway",
                "name": "Circulation::Hallway",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "Circulation::Hallway",
                "name": "Circulation::Hallway",
                "target_lux": 100,
                "target_lux_height": 0.0,
                "watts_per_area": 5.381955,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Circulation::Hallway",
                "name": "Circulation::Hallway",
                "annual_utilization_factor": 0.245833,
            },
            "loads": {
                "identifier": "Circulation::Hallway",
                "name": "Circulation::Hallway",
                "watts_per_area": 0,
            },
        },
    },
    "Classroom": {
        "protocol": "PHIUS",
        "description": "Classroom (school and nursery school)",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::PrimarySchool::Classroom"],
        "people": {
            "schedule": {
                "name": "Classroom",
                "identifier": "Classroom",
                "start_hour": 8,
                "end_hour": 15,
                "annual_utilization_days": 200,
                "relative_utilization_factor": 0.75,
            },
            "loads": {
                "identifier": "Classroom",
                "name": "Classroom",
                "people_per_area": 0.269098,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Classroom",
                "name": "Classroom",
                "daily_operating_hours": 7,
                "annual_utilization_days": 200,
                "relative_utilization_factor": 0.9,
            },
            "loads": {
                "identifier": "Classroom",
                "name": "Classroom",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_area": 7.642369,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Classroom",
                "name": "Classroom",
                "annual_utilization_factor": 0.442427,
            },
            "loads": {
                "identifier": "Classroom",
                "name": "Classroom",
                "watts_per_area": 14.999495,
            },
        },
    },
    "Garage::Private": {
        "protocol": "PHIUS",
        "description": "Garage buildings for offices and private use",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::Courthouse::Parking"],
        "people": {
            "schedule": {
                "name": "Garage::Private",
                "identifier": "Garage::Private",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.05,
            },
            "loads": {
                "identifier": "Garage::Private",
                "name": "Garage::Private",
                "people_per_area": 0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Garage::Private",
                "name": "Garage::Private",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Garage::Private",
                "name": "Garage::Private",
                "target_lux": 75,
                "target_lux_height": 0.0,
                "watts_per_area": 1.614585,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Garage::Private",
                "name": "Garage::Private",
                "annual_utilization_factor": 0.473153,
            },
            "loads": {
                "identifier": "Garage::Private",
                "name": "Garage::Private",
                "watts_per_area": 0,
            },
        },
    },
    "Garage::Public": {
        "protocol": "PHIUS",
        "description": "Garage buildings for public use",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::Courthouse::Parking"],
        "people": {
            "schedule": {
                "name": "Garage::Public",
                "identifier": "Garage::Public",
                "start_hour": 9,
                "end_hour": 24,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 0.2,
            },
            "loads": {
                "identifier": "Garage::Public",
                "name": "Garage::Public",
                "people_per_area": 0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Garage::Public",
                "name": "Garage::Public",
                "daily_operating_hours": 15,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Garage::Public",
                "name": "Garage::Public",
                "target_lux": 100,
                "target_lux_height": 0.0,
                "watts_per_area": 1.614585,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Garage::Public",
                "name": "Garage::Public",
                "annual_utilization_factor": 0.473153,
            },
            "loads": {
                "identifier": "Garage::Public",
                "name": "Garage::Public",
                "watts_per_area": 0,
            },
        },
    },
    "Gym": {
        "protocol": "PHIUS",
        "description": "Sports hall (without public viewing area)",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::SmallHotel::Exercise"],
        "people": {
            "schedule": {
                "name": "Gym",
                "identifier": "Gym",
                "start_hour": 8,
                "end_hour": 23,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 0.7,
            },
            "loads": {
                "identifier": "Gym",
                "name": "Gym",
                "people_per_area": 0.214632,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Gym",
                "name": "Gym",
                "daily_operating_hours": 15,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Gym",
                "name": "Gym",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_area": 9.68751,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Gym",
                "name": "Gym",
                "annual_utilization_factor": 0.4375,
            },
            "loads": {
                "identifier": "Gym",
                "name": "Gym",
                "watts_per_area": 18.621547,
            },
        },
    },
    "Hospital::Ward": {
        "protocol": "PHIUS",
        "description": "Hospital ward or dormitory",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::Hospital::PatRoom"],
        "people": {
            "schedule": {
                "name": "Hospital::Ward",
                "identifier": "Hospital::Ward",
                "start_hour": 8,
                "end_hour": 15,
                "annual_utilization_days": 200,
                "relative_utilization_factor": 0.75,
            },
            "loads": {
                "identifier": "Hospital::Ward",
                "name": "Hospital::Ward",
                "people_per_area": 0.05382,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Hospital::Ward",
                "name": "Hospital::Ward",
                "daily_operating_hours": 7,
                "annual_utilization_days": 200,
                "relative_utilization_factor": 0.5,
            },
            "loads": {
                "identifier": "Hospital::Ward",
                "name": "Hospital::Ward",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_area": 7.319452,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Hospital::Ward",
                "name": "Hospital::Ward",
                "annual_utilization_factor": 0.594292,
            },
            "loads": {
                "identifier": "Hospital::Ward",
                "name": "Hospital::Ward",
                "watts_per_area": 21.5278,
            },
        },
    },
    "Hotel::Bedroom": {
        "protocol": "PHIUS",
        "description": "Hotel bedroom",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::LargeHotel::GuestRoom"],
        "people": {
            "schedule": {
                "name": "Hotel::Bedroom",
                "identifier": "Hotel::Bedroom",
                "start_hour": 21,
                "end_hour": 8,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 0.25,
            },
            "loads": {
                "identifier": "Hotel::Bedroom",
                "name": "Hotel::Bedroom",
                "people_per_area": 0.038427,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Hotel::Bedroom",
                "name": "Hotel::Bedroom",
                "daily_operating_hours": 11,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 0.3,
            },
            "loads": {
                "identifier": "Hotel::Bedroom",
                "name": "Hotel::Bedroom",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_area": 4.413199,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Hotel::Bedroom",
                "name": "Hotel::Bedroom",
                "annual_utilization_factor": 0.315303,
            },
            "loads": {
                "identifier": "Hotel::Bedroom",
                "name": "Hotel::Bedroom",
                "watts_per_area": 6.748965,
            },
        },
    },
    "Kitchen::Commercial::Cooking": {
        "protocol": "PHIUS",
        "description": "Kitchen in non-residential buildings",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::FullServiceRestaurant::Kitchen"],
        "people": {
            "schedule": {
                "name": "Kitchen::Commercial::Cooking",
                "identifier": "Kitchen::Commercial::Cooking",
                "start_hour": 10,
                "end_hour": 23,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Kitchen::Commercial::Cooking",
                "name": "Kitchen::Commercial::Cooking",
                "people_per_area": 0.05382,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Kitchen::Commercial::Cooking",
                "name": "Kitchen::Commercial::Cooking",
                "daily_operating_hours": 13,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Kitchen::Commercial::Cooking",
                "name": "Kitchen::Commercial::Cooking",
                "target_lux": 500,
                "target_lux_height": 0.8,
                "watts_per_area": 11.732651,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Kitchen::Commercial::Cooking",
                "name": "Kitchen::Commercial::Cooking",
                "annual_utilization_factor": 0.164583,
            },
            "loads": {
                "identifier": "Kitchen::Commercial::Cooking",
                "name": "Kitchen::Commercial::Cooking",
                "watts_per_area": 403.969167,
            },
        },
    },
    "Kitchen::Commercial::Prep Room": {
        "protocol": "PHIUS",
        "description": "Kitchen preparation room or storeroom",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::SuperMarket::Deli"],
        "people": {
            "schedule": {
                "name": "Kitchen::Commercial::Prep Room",
                "identifier": "Kitchen::Commercial::Prep Room",
                "start_hour": 7,
                "end_hour": 23,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 0.5,
            },
            "loads": {
                "identifier": "Kitchen::Commercial::Prep Room",
                "name": "Kitchen::Commercial::Prep Room",
                "people_per_area": 0.086111,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Kitchen::Commercial::Prep Room",
                "name": "Kitchen::Commercial::Prep Room",
                "daily_operating_hours": 16,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Kitchen::Commercial::Prep Room",
                "name": "Kitchen::Commercial::Prep Room",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_area": 11.732651,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Kitchen::Commercial::Prep Room",
                "name": "Kitchen::Commercial::Prep Room",
                "annual_utilization_factor": 0.606735,
            },
            "loads": {
                "identifier": "Kitchen::Commercial::Prep Room",
                "name": "Kitchen::Commercial::Prep Room",
                "watts_per_area": 8.934037,
            },
        },
    },
    "Laundry::Public": {
        "protocol": "PHIUS",
        "description": "Common Laundry",
        "source": ["MF_Calculator_2021", "2019::LargeHotel::Laundry"],
        "people": {
            "schedule": {
                "name": "Laundry::Public",
                "identifier": "Laundry::Public",
                "start_hour": 0,
                "end_hour": 24,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Laundry::Public",
                "name": "Laundry::Public",
                "people_per_area": 0.107639,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Laundry::Public",
                "name": "Laundry::Public",
                "daily_operating_hours": 24,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Laundry::Public",
                "name": "Laundry::Public",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_area": 5.704867,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Laundry::Public",
                "name": "Laundry::Public",
                "annual_utilization_factor": 0.447888,
            },
            "loads": {
                "identifier": "Laundry::Public",
                "name": "Laundry::Public",
                "watts_per_area": 61.677147,
            },
        },
    },
    "Library::Reading Room": {
        "protocol": "PHIUS",
        "description": "Library - reading rooms",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::SecondarySchool::Library"],
        "people": {
            "schedule": {
                "name": "Library::Reading Room",
                "identifier": "Library::Reading Room",
                "start_hour": 8,
                "end_hour": 20,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "Library::Reading Room",
                "name": "Library::Reading Room",
                "people_per_area": 0.107639,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Library::Reading Room",
                "name": "Library::Reading Room",
                "daily_operating_hours": 12,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "Library::Reading Room",
                "name": "Library::Reading Room",
                "target_lux": 500,
                "target_lux_height": 0.8,
                "watts_per_area": 8.934037,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Library::Reading Room",
                "name": "Library::Reading Room",
                "annual_utilization_factor": 0.462476,
            },
            "loads": {
                "identifier": "Library::Reading Room",
                "name": "Library::Reading Room",
                "watts_per_area": 10.010427,
            },
        },
    },
    "Library::Storage": {
        "protocol": "PHIUS",
        "description": "Library magazine and stores",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", ""],
        "people": {
            "schedule": {
                "name": "Library::Storage",
                "identifier": "Library::Storage",
                "start_hour": 8,
                "end_hour": 20,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 0.1,
            },
            "loads": {
                "identifier": "Library::Storage",
                "name": "Library::Storage",
                "people_per_area": 0.107639,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Library::Storage",
                "name": "Library::Storage",
                "daily_operating_hours": 12,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Library::Storage",
                "name": "Library::Storage",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_area": 8.934037,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Library::Storage",
                "name": "Library::Storage",
                "annual_utilization_factor": 0.462476,
            },
            "loads": {
                "identifier": "Library::Storage",
                "name": "Library::Storage",
                "watts_per_area": 10.010427,
            },
        },
    },
    "Library::Stacks": {
        "protocol": "PHIUS",
        "description": "Library-open stacks areas",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", ""],
        "people": {
            "schedule": {
                "name": "Library::Stacks",
                "identifier": "Library::Stacks",
                "start_hour": 8,
                "end_hour": 20,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Library::Stacks",
                "name": "Library::Stacks",
                "people_per_area": 0.107639,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Library::Stacks",
                "name": "Library::Stacks",
                "daily_operating_hours": 12,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Library::Stacks",
                "name": "Library::Stacks",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_area": 8.934037,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Library::Stacks",
                "name": "Library::Stacks",
                "annual_utilization_factor": 0.462476,
            },
            "loads": {
                "identifier": "Library::Stacks",
                "name": "Library::Stacks",
                "watts_per_area": 10.010427,
            },
        },
    },
    "Museum::Exhibition": {
        "protocol": "PHIUS",
        "description": "Exhibition rooms and museums with conservation requirements",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::Retail::Retail"],
        "people": {
            "schedule": {
                "name": "Museum::Exhibition",
                "identifier": "Museum::Exhibition",
                "start_hour": 10,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Museum::Exhibition",
                "name": "Museum::Exhibition",
                "people_per_area": 0.161459,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Museum::Exhibition",
                "name": "Museum::Exhibition",
                "daily_operating_hours": 8,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Museum::Exhibition",
                "name": "Museum::Exhibition",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_area": 11.302095,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Museum::Exhibition",
                "name": "Museum::Exhibition",
                "annual_utilization_factor": 0.519583,
            },
            "loads": {
                "identifier": "Museum::Exhibition",
                "name": "Museum::Exhibition",
                "watts_per_area": 3.22917,
            },
        },
    },
    "Mech::Server Room": {
        "protocol": "PHIUS",
        "description": "Server room, computer center",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::MediumOffice::Elec/MechRoom"],
        "people": {
            "schedule": {
                "name": "Mech::Server Room",
                "identifier": "Mech::Server Room",
                "start_hour": 0,
                "end_hour": 24,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 0.5,
            },
            "loads": {
                "identifier": "Mech::Server Room",
                "name": "Mech::Server Room",
                "people_per_area": 0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Mech::Server Room",
                "name": "Mech::Server Room",
                "daily_operating_hours": 24,
                "annual_utilization_days": 365,
                "relative_utilization_factor": 0.5,
            },
            "loads": {
                "identifier": "Mech::Server Room",
                "name": "Mech::Server Room",
                "target_lux": 500,
                "target_lux_height": 0.8,
                "watts_per_area": 4.628477,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Mech::Server Room",
                "name": "Mech::Server Room",
                "annual_utilization_factor": 0.467636,
            },
            "loads": {
                "identifier": "Mech::Server Room",
                "name": "Mech::Server Room",
                "watts_per_area": 2.906253,
            },
        },
    },
    "Manufacturing::Workshop": {
        "protocol": "PHIUS",
        "description": "Workshop, assembly,manufacturing",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::Laboratory::Open lab"],
        "people": {
            "schedule": {
                "name": "Manufacturing::Workshop",
                "identifier": "Manufacturing::Workshop",
                "start_hour": 7,
                "end_hour": 16,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "Manufacturing::Workshop",
                "name": "Manufacturing::Workshop",
                "people_per_area": 0.05382,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Manufacturing::Workshop",
                "name": "Manufacturing::Workshop",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "Manufacturing::Workshop",
                "name": "Manufacturing::Workshop",
                "target_lux": 500,
                "target_lux_height": 0.8,
                "watts_per_area": 14.315987,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Manufacturing::Workshop",
                "name": "Manufacturing::Workshop",
                "annual_utilization_factor": 0.307021,
            },
            "loads": {
                "identifier": "Manufacturing::Workshop",
                "name": "Manufacturing::Workshop",
                "watts_per_area": 43.0556,
            },
        },
    },
    "Office::Meeting Room": {
        "protocol": "PHIUS",
        "description": "Meeting conference and seminar room",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::LargeOffice::Conference"],
        "people": {
            "schedule": {
                "name": "Office::Meeting Room",
                "identifier": "Office::Meeting Room",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.5,
            },
            "loads": {
                "identifier": "Office::Meeting Room",
                "name": "Office::Meeting Room",
                "people_per_area": 0.538196,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Office::Meeting Room",
                "name": "Office::Meeting Room",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Office::Meeting Room",
                "name": "Office::Meeting Room",
                "target_lux": 500,
                "target_lux_height": 0.8,
                "watts_per_area": 10.440983,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Office::Meeting Room",
                "name": "Office::Meeting Room",
                "annual_utilization_factor": 0.512215,
            },
            "loads": {
                "identifier": "Office::Meeting Room",
                "name": "Office::Meeting Room",
                "watts_per_area": 3.982643,
            },
        },
    },
    "Office::Workspace::Open": {
        "protocol": "PHIUS",
        "description": "Landscaped office (seven or more workplaces)",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::LargeOffice::OpenOffice"],
        "people": {
            "schedule": {
                "name": "Office::Workspace::Open",
                "identifier": "Office::Workspace::Open",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "Office::Workspace::Open",
                "name": "Office::Workspace::Open",
                "people_per_area": 0.056511,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Office::Workspace::Open",
                "name": "Office::Workspace::Open",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "Office::Workspace::Open",
                "name": "Office::Workspace::Open",
                "target_lux": 500,
                "target_lux_height": 0.8,
                "watts_per_area": 6.565979,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Office::Workspace::Open",
                "name": "Office::Workspace::Open",
                "annual_utilization_factor": 0.512215,
            },
            "loads": {
                "identifier": "Office::Workspace::Open",
                "name": "Office::Workspace::Open",
                "watts_per_area": 7.642369,
            },
        },
    },
    "Office:Workspace::Medium": {
        "protocol": "PHIUS",
        "description": "Workgroup Office (2-6 workplaces)",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::LargeOffice::ClosedOffice"],
        "people": {
            "schedule": {
                "name": "Office:Workspace::Medium",
                "identifier": "Office:Workspace::Medium",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.7,
            },
            "loads": {
                "identifier": "Office:Workspace::Medium",
                "name": "Office:Workspace::Medium",
                "people_per_area": 0.051129,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Office:Workspace::Medium",
                "name": "Office:Workspace::Medium",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.7,
            },
            "loads": {
                "identifier": "Office:Workspace::Medium",
                "name": "Office:Workspace::Medium",
                "target_lux": 500,
                "target_lux_height": 0.8,
                "watts_per_area": 7.965286,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Office:Workspace::Medium",
                "name": "Office:Workspace::Medium",
                "annual_utilization_factor": 0.512215,
            },
            "loads": {
                "identifier": "Office:Workspace::Medium",
                "name": "Office:Workspace::Medium",
                "watts_per_area": 6.888896,
            },
        },
    },
    "Office::Workspace::Semi-Enclosed": {
        "protocol": "PHIUS",
        "description": "Personal office (single occupant)",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", ""],
        "people": {
            "schedule": {
                "name": "Office::Workspace::Semi-Enclosed",
                "identifier": "Office::Workspace::Semi-Enclosed",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.7,
            },
            "loads": {
                "identifier": "Office::Workspace::Semi-Enclosed",
                "name": "Office::Workspace::Semi-Enclosed",
                "people_per_area": 0.051129,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Office::Workspace::Semi-Enclosed",
                "name": "Office::Workspace::Semi-Enclosed",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.7,
            },
            "loads": {
                "identifier": "Office::Workspace::Semi-Enclosed",
                "name": "Office::Workspace::Semi-Enclosed",
                "target_lux": 500,
                "target_lux_height": 0.8,
                "watts_per_area": 7.965286,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Office::Workspace::Semi-Enclosed",
                "name": "Office::Workspace::Semi-Enclosed",
                "annual_utilization_factor": 0.512215,
            },
            "loads": {
                "identifier": "Office::Workspace::Semi-Enclosed",
                "name": "Office::Workspace::Semi-Enclosed",
                "watts_per_area": 6.888896,
            },
        },
    },
    "Other::Habitable": {
        "protocol": "PHIUS",
        "description": "Other Habitable Room",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::LargeOffice::OpenOffice"],
        "people": {
            "schedule": {
                "name": "Other::Habitable",
                "identifier": "Other::Habitable",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.5,
            },
            "loads": {
                "identifier": "Other::Habitable",
                "name": "Other::Habitable",
                "people_per_area": 0.056511,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Other::Habitable",
                "name": "Other::Habitable",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Other::Habitable",
                "name": "Other::Habitable",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_area": 6.565979,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Other::Habitable",
                "name": "Other::Habitable",
                "annual_utilization_factor": 0.512215,
            },
            "loads": {
                "identifier": "Other::Habitable",
                "name": "Other::Habitable",
                "watts_per_area": 7.642369,
            },
        },
    },
    "Other::Non-Habitable": {
        "protocol": "PHIUS",
        "description": "Auxiliary spaces without habitable rooms",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::LargeOffice::Storage"],
        "people": {
            "schedule": {
                "name": "Other::Non-Habitable",
                "identifier": "Other::Non-Habitable",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.1,
            },
            "loads": {
                "identifier": "Other::Non-Habitable",
                "name": "Other::Non-Habitable",
                "people_per_area": 0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Other::Non-Habitable",
                "name": "Other::Non-Habitable",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Other::Non-Habitable",
                "name": "Other::Non-Habitable",
                "target_lux": 100,
                "target_lux_height": 0.8,
                "watts_per_area": 4.090282,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Other::Non-Habitable",
                "name": "Other::Non-Habitable",
                "annual_utilization_factor": 0.512215,
            },
            "loads": {
                "identifier": "Other::Non-Habitable",
                "name": "Other::Non-Habitable",
                "watts_per_area": 0,
            },
        },
    },
    "Restaurant": {
        "protocol": "PHIUS",
        "description": "Restaurant",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::FullServiceRestaurant::Dining"],
        "people": {
            "schedule": {
                "name": "Restaurant",
                "identifier": "Restaurant",
                "start_hour": 10,
                "end_hour": 24,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Restaurant",
                "name": "Restaurant",
                "people_per_area": 0.753474,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Restaurant",
                "name": "Restaurant",
                "daily_operating_hours": 14,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Restaurant",
                "name": "Restaurant",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_area": 6.45834,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Restaurant",
                "name": "Restaurant",
                "annual_utilization_factor": 0.164583,
            },
            "loads": {
                "identifier": "Restaurant",
                "name": "Restaurant",
                "watts_per_area": 64.927845,
            },
        },
    },
    "Restroom::Public": {
        "protocol": "PHIUS",
        "description": "Toilets and sanitary facilities in non residential buildings",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::MediumOffice::Restroom"],
        "people": {
            "schedule": {
                "name": "Restroom::Public",
                "identifier": "Restroom::Public",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.1,
            },
            "loads": {
                "identifier": "Restroom::Public",
                "name": "Restroom::Public",
                "people_per_area": 0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Restroom::Public",
                "name": "Restroom::Public",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Restroom::Public",
                "name": "Restroom::Public",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_area": 6.781257,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Restroom::Public",
                "name": "Restroom::Public",
                "annual_utilization_factor": 0.467636,
            },
            "loads": {
                "identifier": "Restroom::Public",
                "name": "Restroom::Public",
                "watts_per_area": 2.906253,
            },
        },
    },
    "Retail::Department store": {
        "protocol": "PHIUS",
        "description": "Retail shop/Department store",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::Retail::Core_Retail"],
        "people": {
            "schedule": {
                "name": "Retail::Department store",
                "identifier": "Retail::Department store",
                "start_hour": 8,
                "end_hour": 20,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Retail::Department store",
                "name": "Retail::Department store",
                "people_per_area": 0.161459,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Retail::Department store",
                "name": "Retail::Department store",
                "daily_operating_hours": 12,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Retail::Department store",
                "name": "Retail::Department store",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_area": 11.302095,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Retail::Department store",
                "name": "Retail::Department store",
                "annual_utilization_factor": 0.519583,
            },
            "loads": {
                "identifier": "Retail::Department store",
                "name": "Retail::Department store",
                "watts_per_area": 3.22917,
            },
        },
    },
    "Retail::Grocery": {
        "description": "Retail shop/department store (food department with refrigerated products)",
        "protocol": "PHIUS",
        "description": "",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::SuperMarket::Sales"],
        "people": {
            "schedule": {
                "name": "Retail::Grocery",
                "identifier": "Retail::Grocery",
                "start_hour": 8,
                "end_hour": 20,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Retail::Grocery",
                "name": "Retail::Grocery",
                "people_per_area": 0.086111,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Retail::Grocery",
                "name": "Retail::Grocery",
                "daily_operating_hours": 12,
                "annual_utilization_days": 300,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Retail::Grocery",
                "name": "Retail::Grocery",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_area": 11.302095,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Retail::Grocery",
                "name": "Retail::Grocery",
                "annual_utilization_factor": 0.606735,
            },
            "loads": {
                "identifier": "Retail::Grocery",
                "name": "Retail::Grocery",
                "watts_per_area": 10.979178,
            },
        },
    },
    "Storage::Archive": {
        "protocol": "PHIUS",
        "description": "Storeroom technical equipment room or archive",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::Warehouse::Fine"],
        "people": {
            "schedule": {
                "name": "Storage::Archive",
                "identifier": "Storage::Archive",
                "start_hour": 7,
                "end_hour": 18,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.02,
            },
            "loads": {
                "identifier": "Storage::Archive",
                "name": "Storage::Archive",
                "people_per_area": 0,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Storage::Archive",
                "name": "Storage::Archive",
                "daily_operating_hours": 11,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Storage::Archive",
                "name": "Storage::Archive",
                "target_lux": 100,
                "target_lux_height": 0.8,
                "watts_per_area": 7.427091,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Storage::Archive",
                "name": "Storage::Archive",
                "annual_utilization_factor": 0.427397,
            },
            "loads": {
                "identifier": "Storage::Archive",
                "name": "Storage::Archive",
                "watts_per_area": 0,
            },
        },
    },
    "School::Auditorium": {
        "protocol": "PHIUS",
        "description": "Lecture room, auditorium",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::SecondarySchool::Auditorium"],
        "people": {
            "schedule": {
                "name": "School::Auditorium",
                "identifier": "School::Auditorium",
                "start_hour": 8,
                "end_hour": 18,
                "annual_utilization_days": 150,
                "relative_utilization_factor": 0.75,
            },
            "loads": {
                "identifier": "School::Auditorium",
                "name": "School::Auditorium",
                "people_per_area": 1.614587,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "School::Auditorium",
                "name": "School::Auditorium",
                "daily_operating_hours": 12,
                "annual_utilization_days": 150,
                "relative_utilization_factor": 0.7,
            },
            "loads": {
                "identifier": "School::Auditorium",
                "name": "School::Auditorium",
                "target_lux": 500,
                "target_lux_height": 0.8,
                "watts_per_area": 6.565979,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "School::Auditorium",
                "name": "School::Auditorium",
                "annual_utilization_factor": 0.462476,
            },
            "loads": {
                "identifier": "School::Auditorium",
                "name": "School::Auditorium",
                "watts_per_area": 4.951394,
            },
        },
    },
    "Theater::Seating": {
        "protocol": "PHIUS",
        "description": "Spectators and audience area of theaters and event locations",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::Courthouse::Courtroom"],
        "people": {
            "schedule": {
                "name": "Theater::Seating",
                "identifier": "Theater::Seating",
                "start_hour": 19,
                "end_hour": 23,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Theater::Seating",
                "name": "Theater::Seating",
                "people_per_area": 0.753474,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Theater::Seating",
                "name": "Theater::Seating",
                "daily_operating_hours": 4,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Theater::Seating",
                "name": "Theater::Seating",
                "target_lux": 200,
                "target_lux_height": 0.8,
                "watts_per_area": 12.91668,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Theater::Seating",
                "name": "Theater::Seating",
                "annual_utilization_factor": 0.473153,
            },
            "loads": {
                "identifier": "Theater::Seating",
                "name": "Theater::Seating",
                "watts_per_area": 0,
            },
        },
    },
    "Theater::Lobby": {
        "protocol": "PHIUS",
        "description": "Foyer (theaters and event locations)",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::MediumOffice::Lobby"],
        "people": {
            "schedule": {
                "name": "Theater::Lobby",
                "identifier": "Theater::Lobby",
                "start_hour": 19,
                "end_hour": 23,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.5,
            },
            "loads": {
                "identifier": "Theater::Lobby",
                "name": "Theater::Lobby",
                "people_per_area": 0.107639,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Theater::Lobby",
                "name": "Theater::Lobby",
                "daily_operating_hours": 4,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1,
            },
            "loads": {
                "identifier": "Theater::Lobby",
                "name": "Theater::Lobby",
                "target_lux": 300,
                "target_lux_height": 0.8,
                "watts_per_area": 9.041676,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Theater::Lobby",
                "name": "Theater::Lobby",
                "annual_utilization_factor": 0.467636,
            },
            "loads": {
                "identifier": "Theater::Lobby",
                "name": "Theater::Lobby",
                "watts_per_area": 2.906253,
            },
        },
    },
    "Theater::Stage": {
        "protocol": "PHIUS",
        "description": "Stage (theaters and event locations)",
        "source": ["PHIUS_Certification_Guidebook_v3.02_N10", "2019::MediumOffice::OpenOffice"],
        "people": {
            "schedule": {
                "name": "Theater::Stage",
                "identifier": "Theater::Stage",
                "start_hour": 13,
                "end_hour": 23,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 1.0,
            },
            "loads": {
                "identifier": "Theater::Stage",
                "name": "Theater::Stage",
                "people_per_area": 0.056511,
            },
        },
        "lighting": {
            "schedule": {
                "identifier": "Theater::Stage",
                "name": "Theater::Stage",
                "daily_operating_hours": 10,
                "annual_utilization_days": 250,
                "relative_utilization_factor": 0.6,
            },
            "loads": {
                "identifier": "Theater::Stage",
                "name": "Theater::Stage",
                "target_lux": 1000,
                "target_lux_height": 0.8,
                "watts_per_area": 6.565979,
            },
        },
        "elec_equipment": {
            "schedule": {
                "identifier": "Theater::Stage",
                "name": "Theater::Stage",
                "annual_utilization_factor": 0.467636,
            },
            "loads": {
                "identifier": "Theater::Stage",
                "name": "Theater::Stage",
                "watts_per_area": 10.333344,
            },
        },
    },
}
