from django.core.management.base import BaseCommand
from django.db import transaction

from apps.smart_search.models import Place

from django.contrib.gis.geos import Point
from apps.smart_search.embbeding import create_embedding

LOCATIONS=[
  {
    "title": "Central Library",
    "description": "The central library provides textbooks, reference books, journals, digital resources, reading spaces, and study facilities for students and researchers.",
    "category": "library",
    "latitude": 25.60420,
    "longitude": 88.12782
  },
  {
    "title": "Administrative Building",
    "description": "The administrative building handles university administration, student services, academic records, official documents, and general administrative work.",
    "category": "administration",
    "latitude": 25.60420,
    "longitude": 88.12810
  },
  {
    "title": "Department of Bengali",
    "description": "The Department of Bengali offers academic programs and research opportunities related to Bengali language, literature, culture, and history.",
    "category": "academic",
    "latitude": 25.60420,
    "longitude": 88.12838
  },
  {
    "title": "Department of English",
    "description": "The Department of English provides teaching and research facilities focused on English literature, language, communication, and related studies.",
    "category": "academic",
    "latitude": 25.60420,
    "longitude": 88.12866
  },
  {
    "title": "Department of History",
    "description": "The Department of History supports teaching and research in ancient, medieval, modern, regional, and global history.",
    "category": "academic",
    "latitude": 25.60420,
    "longitude": 88.12894
  },
  {
    "title": "Department of Political Science",
    "description": "The Department of Political Science provides courses and research facilities covering political theory, governance, public administration, and international relations.",
    "category": "academic",
    "latitude": 25.60420,
    "longitude": 88.12922
  },
  {
    "title": "Department of Economics",
    "description": "The Department of Economics focuses on economic theory, statistics, development economics, public policy, and applied economic studies.",
    "category": "academic",
    "latitude": 25.60420,
    "longitude": 88.12950
  },
  {
    "title": "Department of Geography",
    "description": "The Department of Geography provides teaching and research facilities for physical geography, human geography, environmental studies, and geographic analysis.",
    "category": "academic",
    "latitude": 25.60420,
    "longitude": 88.12978
  },
  {
    "title": "Department of Mathematics",
    "description": "The Department of Mathematics offers courses and research opportunities in pure mathematics, applied mathematics, statistics, and mathematical analysis.",
    "category": "academic",
    "latitude": 25.60420,
    "longitude": 88.13006
  },
  {
    "title": "Department of Physics",
    "description": "The Department of Physics provides academic and laboratory facilities for studying mechanics, electronics, optics, thermodynamics, and modern physics.",
    "category": "academic",
    "latitude": 25.60420,
    "longitude": 88.13034
  },
  {
    "title": "Department of Chemistry",
    "description": "The Department of Chemistry provides teaching laboratories and academic facilities for chemical sciences, laboratory experiments, and research.",
    "category": "academic",
    "latitude": 25.60448,
    "longitude": 88.12782
  },
  {
    "title": "Department of Computer Science",
    "description": "The Department of Computer Science provides classrooms, computer laboratories, programming facilities, and academic resources for computing students.",
    "category": "technology",
    "latitude": 25.60448,
    "longitude": 88.12810
  },
  {
    "title": "Computer Laboratory 1",
    "description": "A computer laboratory equipped for programming practice, software development, practical classes, and computer-based academic activities.",
    "category": "laboratory",
    "latitude": 25.60448,
    "longitude": 88.12838
  },
  {
    "title": "Computer Laboratory 2",
    "description": "A practical computing laboratory used for programming exercises, database practice, networking classes, and software-related coursework.",
    "category": "laboratory",
    "latitude": 25.60448,
    "longitude": 88.12866
  },
  {
    "title": "Physics Laboratory",
    "description": "A laboratory used for physics experiments, practical classes, measurements, demonstrations, and undergraduate laboratory work.",
    "category": "laboratory",
    "latitude": 25.60448,
    "longitude": 88.12894
  },
  {
    "title": "Chemistry Laboratory",
    "description": "A laboratory designed for chemistry practical classes, experiments, chemical analysis, demonstrations, and academic research activities.",
    "category": "laboratory",
    "latitude": 25.60448,
    "longitude": 88.12922
  },
  {
    "title": "Geography Laboratory",
    "description": "A practical laboratory supporting cartography, geographic analysis, environmental studies, mapping exercises, and fieldwork preparation.",
    "category": "laboratory",
    "latitude": 25.60448,
    "longitude": 88.12950
  },
  {
    "title": "Seminar Hall",
    "description": "A university seminar hall used for academic seminars, guest lectures, workshops, presentations, conferences, and student activities.",
    "category": "academic",
    "latitude": 25.60448,
    "longitude": 88.12978
  },
  {
    "title": "Auditorium",
    "description": "The university auditorium hosts cultural programs, academic events, conferences, seminars, competitions, and official ceremonies.",
    "category": "culture",
    "latitude": 25.60448,
    "longitude": 88.13006
  },
  {
    "title": "Main Entrance",
    "description": "The primary entrance of the university campus used by students, faculty, staff, visitors, and authorized vehicles.",
    "category": "security",
    "latitude": 25.60448,
    "longitude": 88.13034
  },
  {
    "title": "Main Security Gate",
    "description": "The main security gate manages campus entry and exit, visitor access, vehicle movement, and general campus security.",
    "category": "security",
    "latitude": 25.60476,
    "longitude": 88.12782
  },
  {
    "title": "Security Office",
    "description": "The security office coordinates campus security personnel, visitor management, incident reporting, and access control.",
    "category": "security",
    "latitude": 25.60476,
    "longitude": 88.12810
  },
  {
    "title": "Student Help Desk",
    "description": "The student help desk assists students with general university information, services, directions, forms, and common administrative queries.",
    "category": "student_services",
    "latitude": 25.60476,
    "longitude": 88.12838
  },
  {
    "title": "Examination Office",
    "description": "The examination office manages examination schedules, forms, admit cards, results, examination records, and related student services.",
    "category": "administration",
    "latitude": 25.60476,
    "longitude": 88.12866
  },
  {
    "title": "Accounts Office",
    "description": "The accounts office handles university financial services, fee-related matters, payments, receipts, and financial documentation.",
    "category": "administration",
    "latitude": 25.60476,
    "longitude": 88.12894
  },
  {
    "title": "Registrar Office",
    "description": "The registrar office manages important university administrative records, official correspondence, documentation, and institutional services.",
    "category": "administration",
    "latitude": 25.60476,
    "longitude": 88.12922
  },
  {
    "title": "Vice Chancellor Office",
    "description": "The Vice Chancellor office supports the university's executive administration, official meetings, institutional decisions, and academic leadership.",
    "category": "administration",
    "latitude": 25.60476,
    "longitude": 88.12950
  },
  {
    "title": "Conference Room",
    "description": "A meeting space used by university officials, faculty members, departments, committees, and student organizations for formal discussions.",
    "category": "administration",
    "latitude": 25.60476,
    "longitude": 88.12978
  },
  {
    "title": "Faculty Common Room",
    "description": "A shared space where faculty members can meet, work, discuss academic matters, and take breaks between teaching activities.",
    "category": "student_services",
    "latitude": 25.60476,
    "longitude": 88.13006
  },
  {
    "title": "Student Common Room",
    "description": "A student space intended for relaxation, informal discussions, group activities, and student community interaction.",
    "category": "student_services",
    "latitude": 25.60476,
    "longitude": 88.13034
  },
  {
    "title": "Boys Hostel",
    "description": "A residential facility providing accommodation, common spaces, and basic student amenities for male students.",
    "category": "hostel",
    "latitude": 25.60504,
    "longitude": 88.12782
  },
  {
    "title": "Girls Hostel",
    "description": "A residential facility providing accommodation, common spaces, and basic amenities for female students.",
    "category": "hostel",
    "latitude": 25.60504,
    "longitude": 88.12810
  },
  {
    "title": "Hostel Dining Hall",
    "description": "A dining facility serving meals to residential students and providing a common area for hostel residents.",
    "category": "food",
    "latitude": 25.60504,
    "longitude": 88.12838
  },
  {
    "title": "Hostel Common Room",
    "description": "A shared hostel recreation area where residents can relax, interact, study informally, and participate in group activities.",
    "category": "hostel",
    "latitude": 25.60504,
    "longitude": 88.12866
  },
  {
    "title": "Hostel Warden Office",
    "description": "The warden office manages hostel administration, resident concerns, attendance, discipline, maintenance requests, and accommodation matters.",
    "category": "hostel",
    "latitude": 25.60504,
    "longitude": 88.12894
  },
  {
    "title": "Campus Canteen",
    "description": "A campus food facility where students and staff can purchase snacks, meals, beverages, and other refreshments.",
    "category": "food",
    "latitude": 25.60504,
    "longitude": 88.12922
  },
  {
    "title": "Cafeteria Seating Area",
    "description": "An open seating area near the campus food facilities where students can eat, meet friends, and take breaks.",
    "category": "food",
    "latitude": 25.60504,
    "longitude": 88.12950
  },
  {
    "title": "Medical Centre",
    "description": "A campus health facility intended to provide basic first aid, initial medical assistance, and health-related support to students and staff.",
    "category": "health",
    "latitude": 25.60504,
    "longitude": 88.12978
  },
  {
    "title": "First Aid Room",
    "description": "A designated room for basic first aid and immediate assistance for minor injuries and health emergencies on campus.",
    "category": "health",
    "latitude": 25.60504,
    "longitude": 88.13006
  },
  {
    "title": "Sports Office",
    "description": "The sports office coordinates university sports activities, competitions, team registrations, training programs, and sports events.",
    "category": "sports",
    "latitude": 25.60504,
    "longitude": 88.13034
  },
  {
    "title": "University Playground",
    "description": "An open sports ground used for football, cricket, athletics, recreational activities, training, and university sports events.",
    "category": "sports",
    "latitude": 25.60532,
    "longitude": 88.12782
  },
  {
    "title": "Cricket Ground",
    "description": "A sports field used for cricket practice, matches, student recreation, and university-level sporting activities.",
    "category": "sports",
    "latitude": 25.60532,
    "longitude": 88.12810
  },
  {
    "title": "Football Ground",
    "description": "An open field used for football practice, matches, tournaments, and recreational sports activities.",
    "category": "sports",
    "latitude": 25.60532,
    "longitude": 88.12838
  },
  {
    "title": "Basketball Court",
    "description": "A campus sports court available for basketball practice, matches, physical activity, and student recreation.",
    "category": "sports",
    "latitude": 25.60532,
    "longitude": 88.12866
  },
  {
    "title": "Volleyball Court",
    "description": "A sports court used by students for volleyball practice, matches, tournaments, and recreational activities.",
    "category": "sports",
    "latitude": 25.60532,
    "longitude": 88.12894
  },
  {
    "title": "Open Theatre",
    "description": "An outdoor performance area used for cultural programs, student performances, public events, and university activities.",
    "category": "culture",
    "latitude": 25.60532,
    "longitude": 88.12922
  },
  {
    "title": "Campus Garden",
    "description": "A landscaped campus area providing a quiet environment for relaxation, walking, informal meetings, and recreation.",
    "category": "environment",
    "latitude": 25.60532,
    "longitude": 88.12950
  },
  {
    "title": "Student Activity Centre",
    "description": "A facility supporting student organizations, extracurricular activities, meetings, workshops, and student-led programs.",
    "category": "student_services",
    "latitude": 25.60532,
    "longitude": 88.12978
  },
  {
    "title": "NSS Office",
    "description": "The NSS office coordinates National Service Scheme activities, community service programs, volunteering, awareness campaigns, and student participation.",
    "category": "student_services",
    "latitude": 25.60532,
    "longitude": 88.13006
  },
  {
    "title": "NCC Office",
    "description": "The NCC office supports National Cadet Corps activities, training, discipline programs, camps, and student cadet coordination.",
    "category": "student_services",
    "latitude": 25.60532,
    "longitude": 88.13034
  },
  {
    "title": "Department of Sociology",
    "description": "The Department of Sociology provides academic programs and research opportunities focused on society, social institutions, culture, and social change.",
    "category": "academic",
    "latitude": 25.60560,
    "longitude": 88.12782
  },
  {
    "title": "Department of Philosophy",
    "description": "The Department of Philosophy provides courses and research opportunities covering philosophical thought, ethics, logic, epistemology, and Indian philosophy.",
    "category": "academic",
    "latitude": 25.60560,
    "longitude": 88.12810
  },
  {
    "title": "Department of Education",
    "description": "The Department of Education focuses on teaching, learning, educational theory, pedagogy, curriculum, and educational research.",
    "category": "academic",
    "latitude": 25.60560,
    "longitude": 88.12838
  },
  {
    "title": "Department of Law",
    "description": "The Department of Law provides academic resources and learning facilities related to legal studies, constitutional law, legal theory, and legal practice.",
    "category": "academic",
    "latitude": 25.60560,
    "longitude": 88.12866
  },
  {
    "title": "Department of Commerce",
    "description": "The Department of Commerce provides education in accounting, finance, business management, taxation, economics, and commercial practices.",
    "category": "academic",
    "latitude": 25.60560,
    "longitude": 88.12894
  },
  {
    "title": "Department of Management",
    "description": "The Department of Management focuses on business administration, organizational management, entrepreneurship, marketing, and related subjects.",
    "category": "academic",
    "latitude": 25.60560,
    "longitude": 88.12922
  },
  {
    "title": "Research Centre",
    "description": "A research-focused facility supporting academic research, collaborative projects, scholarly work, and postgraduate research activities.",
    "category": "research",
    "latitude": 25.60560,
    "longitude": 88.12950
  },
  {
    "title": "Digital Learning Centre",
    "description": "A digital learning facility providing computer access, online educational resources, digital courses, and technology-supported learning.",
    "category": "technology",
    "latitude": 25.60560,
    "longitude": 88.12978
  },
  {
    "title": "Language Laboratory",
    "description": "A specialized learning facility supporting language practice, listening exercises, pronunciation training, communication skills, and language learning.",
    "category": "laboratory",
    "latitude": 25.60560,
    "longitude": 88.13006
  },
  {
    "title": "ICT Centre",
    "description": "The ICT centre supports digital services, computer infrastructure, technology facilities, online systems, and campus information technology.",
    "category": "technology",
    "latitude": 25.60560,
    "longitude": 88.13034
  },
  {
    "title": "WiFi Service Centre",
    "description": "A campus support point for wireless network access, connectivity problems, internet account issues, and basic network assistance.",
    "category": "technology",
    "latitude": 25.60588,
    "longitude": 88.12782
  },
  {
    "title": "Computer Repair Desk",
    "description": "A technical support point where students and staff can report computer hardware, software, and basic technical problems.",
    "category": "technology",
    "latitude": 25.60588,
    "longitude": 88.12810
  },
  {
    "title": "Printing and Photocopy Centre",
    "description": "A campus service facility providing printing, photocopying, scanning, and document-related services for students and staff.",
    "category": "student_services",
    "latitude": 25.60588,
    "longitude": 88.12838
  },
  {
    "title": "Stationery Shop",
    "description": "A campus shop providing notebooks, pens, files, folders, academic supplies, and other stationery items for students.",
    "category": "student_services",
    "latitude": 25.60588,
    "longitude": 88.12866
  },
  {
    "title": "Student Service Centre",
    "description": "A centralized facility where students can access information and assistance for common university services and administrative requirements.",
    "category": "student_services",
    "latitude": 25.60588,
    "longitude": 88.12894
  },
  {
    "title": "Admission Office",
    "description": "The admission office handles admission-related information, application support, document verification, and enrollment services.",
    "category": "administration",
    "latitude": 25.60588,
    "longitude": 88.12922
  },
  {
    "title": "Scholarship Office",
    "description": "The scholarship office provides information and administrative support related to student scholarships, financial assistance, and scholarship applications.",
    "category": "student_services",
    "latitude": 25.60588,
    "longitude": 88.12950
  },
  {
    "title": "Career and Placement Cell",
    "description": "The career and placement cell supports internships, recruitment activities, career guidance, placement drives, and employability programs.",
    "category": "student_services",
    "latitude": 25.60588,
    "longitude": 88.12978
  },
  {
    "title": "Alumni Office",
    "description": "The alumni office coordinates alumni engagement, alumni records, networking activities, events, and communication with former students.",
    "category": "student_services",
    "latitude": 25.60588,
    "longitude": 88.13006
  },
  {
    "title": "Training and Development Centre",
    "description": "A facility supporting workshops, skill-development programs, professional training, seminars, and student development activities.",
    "category": "student_services",
    "latitude": 25.60588,
    "longitude": 88.13034
  },
  {
    "title": "Research Scholars Room",
    "description": "A dedicated workspace for research scholars to conduct academic work, access resources, prepare research documents, and collaborate.",
    "category": "research",
    "latitude": 25.60616,
    "longitude": 88.12782
  },
  {
    "title": "Postgraduate Study Centre",
    "description": "A study facility supporting postgraduate students with academic resources, study spaces, and collaborative learning areas.",
    "category": "academic",
    "latitude": 25.60616,
    "longitude": 88.12810
  },
  {
    "title": "Reading Room",
    "description": "A quiet study area where students can read books, prepare for examinations, work on assignments, and study independently.",
    "category": "library",
    "latitude": 25.60616,
    "longitude": 88.12838
  },
  {
    "title": "Digital Library",
    "description": "A digital resource facility providing access to electronic books, journals, databases, online academic materials, and digital learning resources.",
    "category": "library",
    "latitude": 25.60616,
    "longitude": 88.12866
  },
  {
    "title": "Reference Section",
    "description": "A library section containing reference books, encyclopedias, academic materials, and resources intended for research and detailed study.",
    "category": "library",
    "latitude": 25.60616,
    "longitude": 88.12894
  },
  {
    "title": "Library Issue Counter",
    "description": "The library issue counter manages book borrowing, returns, renewals, library membership, and circulation-related services.",
    "category": "library",
    "latitude": 25.60616,
    "longitude": 88.12922
  },
  {
    "title": "Library Help Desk",
    "description": "A support desk where students can ask about library resources, book availability, membership, digital resources, and library services.",
    "category": "library",
    "latitude": 25.60616,
    "longitude": 88.12950
  },
  {
    "title": "Research Journal Section",
    "description": "A library section providing access to academic journals, research publications, scholarly materials, and reference resources.",
    "category": "library",
    "latitude": 25.60616,
    "longitude": 88.12978
  },
  {
    "title": "Group Study Room",
    "description": "A designated room where students can collaborate on projects, discuss academic topics, and conduct group study sessions.",
    "category": "library",
    "latitude": 25.60616,
    "longitude": 88.13006
  },
  {
    "title": "Quiet Study Zone",
    "description": "A quiet library study area intended for individual reading, examination preparation, research, and focused academic work.",
    "category": "library",
    "latitude": 25.60616,
    "longitude": 88.13034
  },
  {
    "title": "Campus Parking Area",
    "description": "A designated parking area for authorized two-wheelers, four-wheelers, faculty vehicles, staff vehicles, and visitors.",
    "category": "parking",
    "latitude": 25.60644,
    "longitude": 88.12782
  },
  {
    "title": "Bicycle Parking",
    "description": "A designated area where students and staff can securely park bicycles while attending classes and other campus activities.",
    "category": "parking",
    "latitude": 25.60644,
    "longitude": 88.12810
  },
  {
    "title": "Visitor Parking",
    "description": "A parking facility intended for visitors and guests attending university meetings, events, academic programs, or administrative work.",
    "category": "parking",
    "latitude": 25.60644,
    "longitude": 88.12838
  },
  {
    "title": "Campus Water Facility",
    "description": "A campus facility supporting drinking water availability and basic water services for students, staff, and visitors.",
    "category": "utilities",
    "latitude": 25.60644,
    "longitude": 88.12866
  },
  {
    "title": "Drinking Water Point",
    "description": "A designated drinking water point where students and staff can access drinking water during campus activities.",
    "category": "utilities",
    "latitude": 25.60644,
    "longitude": 88.12894
  },
  {
    "title": "Public Restroom",
    "description": "A campus restroom facility available for students, staff, and visitors during university activities.",
    "category": "utilities",
    "latitude": 25.60644,
    "longitude": 88.12922
  },
  {
    "title": "Maintenance Office",
    "description": "The maintenance office handles reports related to campus buildings, electrical systems, plumbing, furniture, infrastructure, and repairs.",
    "category": "utilities",
    "latitude": 25.60644,
    "longitude": 88.12950
  },
  {
    "title": "Electrical Maintenance Room",
    "description": "A technical facility supporting campus electrical maintenance, power distribution, equipment inspection, and electrical repairs.",
    "category": "utilities",
    "latitude": 25.60644,
    "longitude": 88.12978
  },
  {
    "title": "Water Pump Facility",
    "description": "A utility facility supporting campus water supply, pumping operations, water distribution, and related maintenance activities.",
    "category": "utilities",
    "latitude": 25.60644,
    "longitude": 88.13006
  },
  {
    "title": "Campus Waste Collection Point",
    "description": "A designated location for temporary collection and management of campus waste before disposal or further processing.",
    "category": "utilities",
    "latitude": 25.60644,
    "longitude": 88.13034
  },
  {
    "title": "Eco Garden",
    "description": "A green campus area designed for environmental awareness, relaxation, biodiversity activities, and student engagement with nature.",
    "category": "environment",
    "latitude": 25.60672,
    "longitude": 88.12782
  },
  {
    "title": "Botanical Area",
    "description": "A campus green space containing plants and vegetation that can support environmental learning, observation, and educational activities.",
    "category": "environment",
    "latitude": 25.60672,
    "longitude": 88.12810
  },
  {
    "title": "Campus Pond",
    "description": "A water body within the campus area that forms part of the university's natural environment and surrounding landscape.",
    "category": "environment",
    "latitude": 25.60672,
    "longitude": 88.12838
  },
  {
    "title": "Open Recreation Area",
    "description": "An outdoor area where students can relax, walk, meet friends, and participate in informal recreational activities.",
    "category": "environment",
    "latitude": 25.60672,
    "longitude": 88.12866
  },
  {
    "title": "Student Event Ground",
    "description": "An open campus area used for student events, awareness programs, cultural activities, exhibitions, and outdoor gatherings.",
    "category": "culture",
    "latitude": 25.60672,
    "longitude": 88.12894
  },
  {
    "title": "Cultural Activity Centre",
    "description": "A facility supporting music, dance, drama, cultural clubs, student performances, competitions, and cultural programs.",
    "category": "culture",
    "latitude": 25.60672,
    "longitude": 88.12922
  },
  {
    "title": "Music Practice Room",
    "description": "A designated room for students involved in music practice, rehearsals, cultural programs, and university performances.",
    "category": "culture",
    "latitude": 25.60672,
    "longitude": 88.12950
  },
  {
    "title": "Drama Practice Room",
    "description": "A practice space for theatre groups and students preparing stage performances, plays, cultural programs, and drama competitions.",
    "category": "culture",
    "latitude": 25.60672,
    "longitude": 88.12978
  },
  {
    "title": "Student Club Room",
    "description": "A shared facility where registered student clubs can conduct meetings, planning sessions, workshops, and extracurricular activities.",
    "category": "culture",
    "latitude": 25.60672,
    "longitude": 88.13006
  },
  {
    "title": "University Guest House",
    "description": "A university accommodation facility intended for visiting faculty, academic guests, officials, researchers, and invited visitors.",
    "category": "hostel",
    "latitude": 25.60672,
    "longitude": 88.13034
  }
]



class Command(BaseCommand):
    help = "Seed campus locations"

    def handle(self, *args, **options):

        for data in LOCATIONS:

            try:
                with transaction.atomic():

                    latitude=data['latitude']

                    longitude=data['longitude']

                    place = Point(longitude,latitude,srid=4326)
                    embedding=create_embedding(title=data["title"],description=data["description"],category=data['category'])

                    location = Place.objects.create(
                            name=data["title"],
                            description=data["description"],
                            category=data['category'],
                            location=place,
                            embedding=embedding
                        )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Saved: {location.name}"
                    )
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Failed: {data['title']} -> {e}"
                    )
                )
                break