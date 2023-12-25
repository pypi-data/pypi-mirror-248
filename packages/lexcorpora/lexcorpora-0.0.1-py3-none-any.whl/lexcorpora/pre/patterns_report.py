from typing import Any

covered = {"TEXT": {"REGEX": "^\\(\\d+\\)$"}, "OP": "?"}

publisher_short = {"ORTH": {"IN": ["SCRA", "Phil", "Phil.", "Phil.,", "OG", "O.G."]}}

publisher_words_phil = [
    {"ORTH": {"IN": ["Phil", "Phil.", "Phil.,"]}},
    {"ORTH": {"IN": ["Rep", "Rep.", "Rep.," "Reports"]}},
]

publisher_words_og = [
    {"ORTH": {"IN": ["Off", "Off."]}},
    {"ORTH": {"IN": ["Gaz", "Gazette"]}},
]

generic_start: list[dict[str, Any]] = [
    {"IS_DIGIT": True},
    publisher_short,
    {"ORTH": {"IN": ["at", "p", "p.", ","]}, "OP": "?"},
]

generic_start_phil_words = (
    [{"IS_DIGIT": True}] + publisher_words_phil + [{"ORTH": {"IN": ["at", "p", "p.", ","]}, "OP": "?"}]
)

generic_start_og_words = (
    [{"IS_DIGIT": True}] + publisher_words_og + [{"ORTH": {"IN": ["at", "p", "p.", ","]}, "OP": "?"}]
)

special_volumes: list[dict[str, Any]] = [
    {"ORTH": {"IN": ["258-A", "290-A", "8-A"]}},  # Dashed letter vs. digit
    publisher_short,
    {"IS_DIGIT": True},
]

connected_comma_pages: list[dict[str, Any]] = [
    {"IS_DIGIT": True},
    publisher_short,
    {"TEXT": {"REGEX": "\\d+[,-]\\d+"}},  # 21 Phil 124,125
]

og_legacy: list[dict[str, Any]] = [
    {"IS_DIGIT": True},
    covered,
    {"ORTH": {"IN": ["OG", "O.G."]}},
    covered,
]

US_PUBLISHERS = """
A.D.2d
A.D.3d
A.L.R.
A.L.R.,
A.L.R.2d
A.L.R.3d
A.L.R.4th
A.M.C.
A.M.C.,
Alaska
Allen,
Am.S.R.
Am.St.Rep.
App.Div.
Ariz.,
B.T.A.
Bail.,
Barb.,
Binn.,
Biss.,
Black,
Blackf.
Blatchf.,
Bond.,
Bosw.,
Boyce,
Brock.
Brock.,
C.C.A.
C.C.A.,
C.C.P.A.
C.J.S.
C.M.R.
Cal.2d
Cal.2d,
Cal.3d
Cal.App.
Cal.App.2d
Cal.App.3d
Cal.App.4th
Cal.Rptr.
Cal.Rptr.2d
Cal.Rptr.3d
Chip.,
Cliff.
Cliff.,
Colo.,
Commw.
Conn.,
Conn.App.
Cranch
Cranch,
Crim.,
Ct.Cl.
Cush.,
Cushing,
Dakota,
Dall.,
Dallas
Dallas,
Denio,
Dill.,
F.C.C.2d
F.R.D.
F.Supp.
F.Supp.2d
F.Supp.3d
Fed.R.Serv.2d
Fed.R.Serv.3d
Flip.,
Florida,
Ga.App.
Gilman,
Gratt.
Harr.,
Hawaii
Hawaii,
Hawks,
Heisk.,
Hilt.,
Howard
Howard,
Humph.,
Idaho,
Ill.2d
Ill.App.
Ill.App.2d
Ill.App.3d
Ill.Dec.
Johns.
Johns.,
Johnson,
Kan.App.2d
Kans.,
Keyes,
L.E.2d
L.Ed.,
L.Ed.2d
L.J.Q.B.
L.R.A.
L.R.A.,
L.R.A.N.S.
L.R.R.M.
L.ed.155,
Leigh,
MacArth.
Mackey
Martin,
Mason,
Mass.,
McAll.,
McCrary
McCrary,
McLean
McLean,
Md.App.
Metc.,
Mich.,
Minn.,
Misc.,
Misc.2d
Miss.,
Mont.,
N.C.App.
N.E.2d
N.E.2d,
N.E.3d
N.J.L.
N.J.L.,
N.J.Law
N.J.Super.
N.L.R.B.,
N.W.2d
N.W.2d.
N.Y.2d
N.Y.Civ.Proc.R.
N.Y.Crim.R.
N.Y.S.
N.Y.S.,
N.Y.S.2d
N.Y.St.Rep.
O.C.D.
Okl.Cr.
Okla.,
Or.App.
Oreg.,
P.2d.,
P.U.R.
Pa.Cmwlth.
Pacific
Pacific,
Paige,
Paine,
Penn.,
Peters
Peters,
Phil.,
Phila.,
Pick.,
Port.,
Porter,
Rptr.,
S.C.R.
S.Ct.,
S.E.2d
S.W.2d
S.W.2d.
S.W.3d
Sawy.,
Scam.,
Sickels
Sneed,
South,
South.
South.,
State,
Story,
Strob.,
Sumn.,
Sup.Ct.,
Super,
Super.
Super.,
Supp.,
Sweeny,
Tenn.,
Tenn.App.
Tex.Cr.R.
Texas,
Thompson
Tyler,
U.S.L.W.
U.S.P.Q.
U.S.P.Q.2d
Vroom,
Wall.,
Wash.,
Wash.2d
Wash.App.
Wend.,
Wendell,
Whart.,
Wheat.
Wheat.,
Wheaton
Wheaton,
Will.,
Woods,
Yerg.,
"""
"""See text/report_publisher_variants.txt"""


def create_short_publisher_doc():
    for node in [{"IS_DIGIT": True}, {"TEXT": {"REGEX": "\\d+[,-]\\d+"}}]:
        yield [{"IS_DIGIT": True}, {"ORTH": {"IN": US_PUBLISHERS.splitlines()}, "OP": "{1,4}"}, node]


patterns_report_foreign: list[list[dict[str, Any]]] = list(create_short_publisher_doc())


patterns_report: list[list[dict[str, Any]]] = [
    generic_start + [{"IS_DIGIT": True}],
    generic_start + [{"TEXT": {"REGEX": "\\d+[,-]\\d+"}}],
    generic_start_phil_words + [{"IS_DIGIT": True}],
    generic_start_phil_words + [{"TEXT": {"REGEX": "\\d+[,-]\\d+"}}],
    generic_start_og_words + [{"IS_DIGIT": True}],
    generic_start_og_words + [{"TEXT": {"REGEX": "\\d+[,-]\\d+"}}],
    connected_comma_pages,
    special_volumes,
    og_legacy + [{"IS_DIGIT": True}],
    og_legacy + [{"LIKE_NUM": True}],  # e.g. fourth, fifth
]
