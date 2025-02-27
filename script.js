// Initialize 
const canvas = document.createElement('canvas');
const context = canvas.getContext('2d');
document.body.appendChild(canvas);

const clock = { tick: (fps) => setTimeout(() => {}, 1000 / fps) };

// Create a window
canvas.width = 1240;
canvas.height = 930;
document.title = 'TCHS Interactive Map';

// Load map
const mapImage = new Image();
mapImage.src = 'graphics/map_copy.png';

// Load images of school
// Red
const rm601Image = new Image();
rm601Image.src = 'graphics/601.png';
const staffLoungeImage = new Image();
staffLoungeImage.src = 'graphics/staff_lounge.png';
const rm_216_image = new Image();
rm_216_image.src = 'graphics/214.png'
const rm_215_image = new Image();
rm_215_image.src = 'graphics/214.png';
const rm_214_image = new Image();
rm_214_image.src = 'graphics/214.png';
const RR_1_image = new Image();
RR_1_image.src = 'graphics/214.png';
const rm_116_image = new Image();
rm_116_image.src = 'graphics/116.png';
const rm_115_image = new Image();
rm_115_image.src = 'graphics/115.png';
const rm_114_image = new Image();
rm_114_image.src = 'graphics/114.png';
const RR_2_image = new Image();
RR_2_image.src = 'graphics/601.png';
const rm_213_image = new Image();
rm_213_image.src = 'graphics/213.png';
const rm_113_image = new Image();
rm_113_image.src = 'graphics/113.png';
const rm_108_image = new Image();
rm_108_image.src = 'graphics/108.png';
const rm_208_image = new Image();
rm_208_image.src = 'graphics/208.png';
const rm_212_image = new Image();
rm_212_image.src = 'graphics/601.png';
const rm_211_image = new Image();
rm_211_image.src = 'graphics/601.png';
const rm_210_image = new Image();
rm_210_image.src = 'graphics/601.png';
const rm_209_image = new Image();
rm_209_image.src = 'graphics/601.png';
const RR_3_image = new Image();
RR_3_image.src = 'graphics/601.png';
const rm_112_image = new Image();
rm_112_image.src = 'graphics/601.png';
const rm_111_image = new Image();
rm_111_image.src = 'graphics/601.png';
const rm_110_image = new Image();
rm_110_image.src = 'graphics/110.png';
const rm_109_image = new Image();
rm_109_image.src = 'graphics/601.png';
const RR_4_image = new Image();
RR_4_image.src = 'graphics/601.png';
// Red
// Purple
const RR_400_image = new Image();
RR_400_image.src = 'graphics/boys_ bathroom_200s.png';
const rm_401_image = new Image();
rm_401_image.src = 'graphics/ROOM 401-1.PNG';
const rm_402_image = new Image();
rm_402_image.src = 'graphics/ROOM 402-2.PNG';
const rm_403_image = new Image();
rm_403_image.src = 'graphics/ROOM 403-1.PNG';
const rm_404_image = new Image();
rm_404_image.src = 'graphics/ROOM 404-1.PNG';
const rm_405_image = new Image();
rm_405_image.src = 'graphics/ROOM 405-1.PNG';
const rm_406_image = new Image();
rm_406_image.src = 'graphics/ROOM 406-1.PNG';
const rm_407_image = new Image();
rm_407_image.src = 'graphics/ROOM 407-1.PNG';
const rm_408_image = new Image();
rm_408_image.src = 'graphics/ROOM 408-1.PNG';
const rm_409_image = new Image();
rm_409_image.src = 'graphics/ROOM 409-1.PNG';
const rm_410_image = new Image();
rm_410_image.src = 'graphics/ROOM 410-1.PNG';
// Purple
// Green
const gym_image = new Image();
gym_image.src = 'graphics/Front Entrance to Gym.png';
const tennis_image = new Image();
tennis_image.src = 'graphics/Tennis Courts.png';
const rm_702_image = new Image();
rm_702_image.src = 'graphics/Room 702 and Tennis Court Entrance.png';
const circle_image = new Image();
circle_image.src = 'graphics/Senior Circle_1.png';
const rm_703_image = new Image();
rm_703_image.src = 'graphics/601.png';
const rm_704_image = new Image();
rm_704_image.src = 'graphics/700s side and gym stairs.png';
const rm_705_image = new Image();
rm_705_image.src = 'graphics/room 705 (edt) and 704.png';
const rm_706_image = new Image();
rm_706_image.src = 'graphics/room 706 and 707.png';
const rm_707_image = new Image();
rm_707_image.src = 'graphics/room 707.png';
const rm_708_image = new Image();
rm_708_image.src = 'graphics/601.png';
const rm_709_image = new Image();
rm_709_image.src = 'graphics/Boys restroom and art room.png';
const rm_801_image = new Image();
rm_801_image.src = 'graphics/601.png';
const rm_802_image = new Image();
rm_802_image.src = 'graphics/601.png';
const rr_1_image = new Image();
rr_1_image.src = 'graphics/room 707 windows and girls restroom.png';
const weight_image = new Image();
weight_image.src = 'graphics/Weight Room.png';
// Green
// Yellow
const rm_501_image = new Image();
rm_501_image.src = 'graphics/rm_501.png';
const rm_502_image = new Image();
rm_502_image.src = 'graphics/rm_502.png';
const rm_503_image = new Image();
rm_503_image.src = 'graphics/rm_503.png';
const rm_504_image = new Image();
rm_504_image.src = 'graphics/rm_504.png';
const rm_505_image = new Image();
rm_505_image.src = 'graphics/rm_505.png';
const rm_506_image = new Image();
rm_506_image.src = 'graphics/rm_506.png';
const rm_507_image = new Image();
rm_507_image.src = 'graphics/rm_507.png';
const rm_508_image = new Image();
rm_508_image.src = 'graphics/rm_508.png';
const rm_509_image = new Image();
rm_509_image.src = 'graphics/rm_509.png';
const rm_510_image = new Image();
rm_510_image.src = 'graphics/rm_510.png';
const rm_511_image = new Image();
rm_511_image.src = 'graphics/rm_511.png';
const rm_512_image = new Image();
rm_512_image.src = 'graphics/rm_512.png';
const rm_514_image = new Image();
rm_514_image.src = 'graphics/rm_514.png';
const rm_515_image = new Image();
rm_515_image.src = 'graphics/rm_515.png';
const rm_516_image = new Image();
rm_516_image.src = 'graphics/rm_516.png';
const rm_517_image = new Image();
rm_517_image.src = 'graphics/rm_517.png';
const RR_yellow_image = new Image();
RR_yellow_image.src = 'graphics/601.png';
// Yellow
// Blue
const rm_905_image = new Image();
rm_905_image.src = 'graphics/601 Entrance.PNG';
const rm_904_image = new Image();
rm_904_image.src = 'graphics/601 Entrance.PNG';
const tennis_courts_image = new Image();
tennis_courts_image.src = 'graphics/601 Entrance.PNG';
const lemon_parking_lot_image = new Image();
lemon_parking_lot_image.src = 'graphics/601 Entrance.PNG';
const lawn_image = new Image();
lawn_image.src = 'graphics/601 Entrance.PNG';
const media_center_image = new Image();
media_center_image.src = 'graphics/601 Entrance.PNG';
const senate_room_image = new Image();
senate_room_image.src = 'graphics/601 Entrance.PNG';
const mc4_image = new Image();
mc4_image.src = 'graphics/601 Entrance.PNG';
const mc3_image = new Image();
mc3_image.src = 'graphics/601 Entrance.PNG';
const mc2_image = new Image();
mc2_image.src = 'graphics/601 Entrance.PNG';
const mc1_image = new Image();
mc1_image.src = 'graphics/601 Entrance.PNG';
// Blue
// Orange
const principal_office = new Image();
principal_office.src = 'graphics/principal_s_office.png';
const nurse = new Image();
nurse.src = 'graphics/nurse_s_office.png';
const registrar = new Image();
registrar.src = 'graphics/601.png';
const conference_room = new Image();
conference_room.src = 'graphics/conference_room.png';
const rm_311 = new Image();
rm_311.src = 'graphics/311_staff_entrance.png';
const attendance_office = new Image();
attendance_office.src = 'graphics/attendance_office_inner_entrance.png';
const rm_310 = new Image();
rm_310.src = 'graphics/rm_310.png';
const ccc = new Image();
ccc.src = 'graphics/counseling_office.png';
const rm_304 = new Image();
rm_304.src = 'graphics/rm_304.png';
const rr_orange = new Image();
rr_orange.src = 'graphics/601.png';
const rm_309 = new Image();
rm_309.src = 'graphics/601.png';
const rm_308 = new Image();
rm_308.src = 'graphics/601.png';
const rm_305 = new Image();
rm_305.src = 'graphics/rm_305.png';
const rm_306 = new Image();
rm_306.src = 'graphics/rm_306.png';
const rm_307 = new Image();
rm_307.src = 'graphics/rm_307.png';
const lunch = new Image();
lunch.src = 'graphics/601.png';
// Orange
// Brown
const rm_101_image = new Image();
rm_101_image.src = 'graphics/rm_101.png';
const rm_102_image = new Image();
rm_102_image.src = 'graphics/rm_102.png';
const rm_103_image = new Image();
rm_103_image.src = 'graphics/rm_103.png';
const rm_104_image = new Image();
rm_104_image.src = 'graphics/rm_104.png';
const rm_105_image = new Image();
rm_105_image.src = 'graphics/rm_105.png';
const rm_106_image = new Image();
rm_106_image.src = 'graphics/rm_106.png';
const rm_107_image = new Image();
rm_107_image.src = 'graphics/rm_107.png';
const rm_201_image = new Image();
rm_201_image.src = 'graphics/rm_201.png';
const rm_202_image = new Image();
rm_202_image.src = 'graphics/rm_202.png';
const rm_203_image = new Image();
rm_203_image.src = 'graphics/rm_203.png';
const rm_204_image = new Image();
rm_204_image.src = 'graphics/rm_204.png';
const rm_205_image = new Image();
rm_205_image.src = 'graphics/rm_205.png';
const rm_206_image = new Image();
rm_206_image.src = 'graphics/rm_206.png';
const rm_207_image = new Image();
rm_207_image.src = 'graphics/rm_207.png';
const rm_804_image = new Image();
rm_804_image.src = 'graphics/rm_804.png';
const rm_805_image = new Image();
rm_805_image.src = 'graphics/601.png';
const locker_image = new Image();
locker_image.src = 'graphics/locker.png';
const pool_image = new Image();
pool_image.src = 'graphics/pool.png';
// Brown

// Create current screen variable
let currentScreen = mapImage;

// Create a font object
// Red
const fontRegular33 = '33px Arial';
const fontRegular25 = '25px Arial';
// Purple
const fontPurple30 = '30px Arial';
const fontPurple20 = '20px Arial';
// Green
const fontGreen20 = '20px Arial';
const fontGreen15 = '15px Arial';
// Yellow
const fontYellow30 = '30px Arial';
const fontYellow20 = '20px Arial';
// Blue
const fontBlue25 = '25px Arial';
const fontBlue16 = '16px Arial';
// Orange
const fontOrange13 = '13px Arial';
const fontOrange30 = '30px Arial';
const fontOrange20 = '20px Arial';
const fontOrange18 = '18px Arial';
const fontOrange27 = '27px Arial';
const fontNurse28 = '28px Arial';
const fontRgr28 = '28px Arial';

// Create a surface for the button
// Red
const rm601ButtonSurface = { width: 50, height: 25 };
const staffLoungeButtonSurface = { width: 115, height: 51 };
const rm216ButtonSurface = { width: 50, height: 25 };
const rm215ButtonSurface = { width: 50, height: 25 };
const rm214ButtonSurface = { width: 50, height: 25 };
const RR1ButtonSurface = { width: 50, height: 25 };
const rm116ButtonSurface = { width: 50, height: 25 };
const rm115ButtonSurface = { width: 50, height: 25 };
const rm114ButtonSurface = { width: 50, height: 25 };
const RR2ButtonSurface = { width: 50, height: 25 };
const rm213ButtonSurface = { width: 50, height: 25 };
const rm113ButtonSurface = { width: 50, height: 25 };
const rm108ButtonSurface = { width: 50, height: 25 };
const rm208ButtonSurface = { width: 50, height: 25 };
const rm212ButtonSurface = { width: 50, height: 25 };
const rm211ButtonSurface = { width: 50, height: 25 };
const rm210ButtonSurface = { width: 50, height: 25 };
const rm209ButtonSurface = { width: 50, height: 25 };
const RR3ButtonSurface = { width: 50, height: 25 };
const rm112ButtonSurface = { width: 50, height: 25 };
const rm111ButtonSurface = { width: 50, height: 25 };
const rm110ButtonSurface = { width: 50, height: 25 };
const rm109ButtonSurface = { width: 50, height: 25 };
const RR4ButtonSurface = { width: 50, height: 25 };
// Red

// Purple
const RR400ButtonSurface = { width: 36, height: 10 };
const rm401ButtonSurface = { width: 36, height: 44 };
const rm402ButtonSurface = { width: 36, height: 44 };
const rm403ButtonSurface = { width: 36, height: 44 };
const rm404ButtonSurface = { width: 36, height: 44 };
const rm405ButtonSurface = { width: 36, height: 44 };
const rm406ButtonSurface = { width: 36, height: 44 };
const rm407ButtonSurface = { width: 36, height: 44 };
const rm408ButtonSurface = { width: 36, height: 44 };
const rm409ButtonSurface = { width: 36, height: 44 };
const rm410ButtonSurface = { width: 36, height: 44 };
// Purple

// Green
const gymButtonSurface = { width: 70, height: 50 };
const tennisButtonSurface = { width: 39, height: 50 };
const circleButtonSurface = { width: 49, height: 33 };
const rm702ButtonSurface = { width: 50, height: 25 };
const rm703ButtonSurface = { width: 48, height: 25 };
const rm705ButtonSurface = { width: 23, height: 25 };
const rm704ButtonSurface = { width: 23, height: 25 };
const rm706ButtonSurface = { width: 21, height: 25 };
const rm707ButtonSurface = { width: 21, height: 25 };
const rm708ButtonSurface = { width: 21, height: 25 };
const rm709ButtonSurface = { width: 25, height: 22 };
const rm801ButtonSurface = { width: 22, height: 25 };
const rm802ButtonSurface = { width: 22, height: 25 };
const rr1ButtonSurface = { width: 21, height: 25 };
const weightButtonSurface = { width: 30, height: 20 };
// Green

// Yellow
const rm501ButtonSurface = { width: 35, height: 25 };
const rm502ButtonSurface = { width: 37, height: 25 };
const rm503ButtonSurface = { width: 37, height: 25 };
const rm504ButtonSurface = { width: 37, height: 25 };
const rm505ButtonSurface = { width: 36, height: 25 };
const rm506ButtonSurface = { width: 35, height: 25 };
const rm507ButtonSurface = { width: 35, height: 25 };
const rm508ButtonSurface = { width: 38, height: 25 };
const rm509ButtonSurface = { width: 38.5, height: 25 };
const rm510ButtonSurface = { width: 35, height: 25 };
const rm511ButtonSurface = { width: 35, height: 25 };
const rm512ButtonSurface = { width: 35, height: 25 };
const rm514ButtonSurface = { width: 35, height: 25 };
const rm515ButtonSurface = { width: 35, height: 25 };
const rm516ButtonSurface = { width: 35, height: 25 };
const rm517ButtonSurface = { width: 35, height: 25 };
const RRYellowButtonSurface = { width: 35, height: 10.5 };
// Yellow

// Blue
const rm905ButtonSurface = { width: 50, height: 25 };
const rm904ButtonSurface = { width: 50, height: 25 };
const tennisCourtsButtonSurface = { width: 120, height: 25 };
const lemonParkingLotButtonSurface = { width: 124, height: 50 };
const lawnButtonSurface = { width: 70, height: 35 };
const mediaCenterButtonSurface = { width: 120, height: 25 };
const senateRoomButtonSurface = { width: 80, height: 25 };
const mc1ButtonSurface = { width: 40, height: 25 };
const mc2ButtonSurface = { width: 40, height: 25 };
const mc3ButtonSurface = { width: 40, height: 25 };
const mc4ButtonSurface = { width: 40, height: 25 };
// Blue

// Orange
const POButtonSurface = { width: 43, height: 35 };
const nurseButtonSurface = { width: 36, height: 24 };
const rgrButtonSurface = { width: 38, height: 24 };
const confButtonSurface = { width: 43, height: 35 };
const lunchButtonSurface = { width: 65, height: 30 };
// Orange

// Brown
const poolButtonSurface = { width: 50, height: 25 };
const lockerRoomsButtonSurface = { width: 50, height: 25 };
const rm101ButtonSurface = { width: 50, height: 25 };
// Brown

// Back
const backButtonSurface = { width: 100, height: 50 };
// Back


// Render text on the button

// Red
const rm601Text = '601';
const rm601TextRect = { x: rm601ButtonSurface.width / 2, y: rm601ButtonSurface.height / 2 };

const staffLoungeText = 'Staff Lounge';
const staffLoungeTextRect = { x: staffLoungeButtonSurface.width / 2, y: staffLoungeButtonSurface.height / 2 };

const rm216Text = '216';
const rm216TextRect = { x: rm216ButtonSurface.width / 2, y: rm216ButtonSurface.height / 2 };

const rm215Text = '215';
const rm215TextRect = { x: rm215ButtonSurface.width / 2, y: rm215ButtonSurface.height / 2 };

const rm214Text = '214';
const rm214TextRect = { x: rm214ButtonSurface.width / 2, y: rm214ButtonSurface.height / 2 };

const RR1Text = 'RR';
const RR1TextRect = { x: RR1ButtonSurface.width / 2, y: RR1ButtonSurface.height / 2 };

const rm116Text = '116';
const rm116TextRect = { x: rm116ButtonSurface.width / 2, y: rm116ButtonSurface.height / 2 };

const rm115Text = '115';
const rm115TextRect = { x: rm115ButtonSurface.width / 2, y: rm115ButtonSurface.height / 2 };

const rm114Text = '114';
const rm114TextRect = { x: rm114ButtonSurface.width / 2, y: rm114ButtonSurface.height / 2 };

const RR2Text = 'RR';
const RR2TextRect = { x: RR2ButtonSurface.width / 2, y: RR2ButtonSurface.height / 2 };

const rm213Text = '213';
const rm213TextRect = { x: rm213ButtonSurface.width / 2, y: rm213ButtonSurface.height / 2 };

const rm113Text = '113';
const rm113TextRect = { x: rm113ButtonSurface.width / 2, y: rm113ButtonSurface.height / 2 };

const rm108Text = '108';
const rm108TextRect = { x: rm108ButtonSurface.width / 2, y: rm108ButtonSurface.height / 2 };

const rm208Text = '208';
const rm208TextRect = { x: rm208ButtonSurface.width / 2, y: rm208ButtonSurface.height / 2 };

const rm212Text = '212';
const rm212TextRect = { x: rm212ButtonSurface.width / 2, y: rm212ButtonSurface.height / 2 };

const rm211Text = '211';
const rm211TextRect = { x: rm211ButtonSurface.width / 2, y: rm211ButtonSurface.height / 2 };

const rm210Text = '210';
const rm210TextRect = { x: rm210ButtonSurface.width / 2, y: rm210ButtonSurface.height / 2 };

const rm209Text = '209';
const rm209TextRect = { x: rm209ButtonSurface.width / 2, y: rm209ButtonSurface.height / 2 };

const RR3Text = 'RR';
const RR3TextRect = { x: RR3ButtonSurface.width / 2, y: RR3ButtonSurface.height / 2 };

const rm112Text = '112';
const rm112TextRect = { x: rm112ButtonSurface.width / 2, y: rm112ButtonSurface.height / 2 };

const rm111Text = '111';
const rm111TextRect = { x: rm111ButtonSurface.width / 2, y: rm111ButtonSurface.height / 2 };

const rm110Text = '110';
const rm110TextRect = { x: rm110ButtonSurface.width / 2, y: rm110ButtonSurface.height / 2 };

const rm109Text = '109';
const rm109TextRect = { x: rm109ButtonSurface.width / 2, y: rm109ButtonSurface.height / 2 };

const RR4Text = 'RR';
const RR4TextRect = { x: RR4ButtonSurface.width / 2, y: RR4ButtonSurface.height / 2 };
// Red
// Purple
const RR400Text = 'RR';
const RR400TextRect = { x: RR400ButtonSurface.width / 2, y: RR400ButtonSurface.height / 2 };

const rm401Text = '401';
const rm401TextRect = { x: rm401ButtonSurface.width / 2, y: rm401ButtonSurface.height / 2 };

const rm402Text = '402';
const rm402TextRect = { x: rm402ButtonSurface.width / 2, y: rm402ButtonSurface.height / 2 };

const rm403Text = '403';
const rm403TextRect = { x: rm403ButtonSurface.width / 2, y: rm403ButtonSurface.height / 2 };

const rm404Text = '404';
const rm404TextRect = { x: rm404ButtonSurface.width / 2, y: rm404ButtonSurface.height / 2 };

const rm405Text = '405';
const rm405TextRect = { x: rm405ButtonSurface.width / 2, y: rm405ButtonSurface.height / 2 };

const rm406Text = '406';
const rm406TextRect = { x: rm406ButtonSurface.width / 2, y: rm406ButtonSurface.height / 2 };

const rm407Text = '407';
const rm407TextRect = { x: rm407ButtonSurface.width / 2, y: rm407ButtonSurface.height / 2 };

const rm408Text = '408';
const rm408TextRect = { x: rm408ButtonSurface.width / 2, y: rm408ButtonSurface.height / 2 };

const rm409Text = '409';
const rm409TextRect = { x: rm409ButtonSurface.width / 2, y: rm409ButtonSurface.height / 2 };

const rm410Text = '410';
const rm410TextRect = { x: rm410ButtonSurface.width / 2, y: rm410ButtonSurface.height / 2 };
// Purple
// Green
const gymText = 'Gym';
const gymTextRect = { x: gymButtonSurface.width / 2, y: gymButtonSurface.height / 2 };

const tennisText = 'Tennis';
const tennisTextRect = { x: tennisButtonSurface.width / 2, y: tennisButtonSurface.height / 2 };

const rm702Text = '702';
const rm702TextRect = { x: rm702ButtonSurface.width / 2, y: rm702ButtonSurface.height / 2 };

const circleText = 'Sr. Circle';
const circleTextRect = { x: circleButtonSurface.width / 2, y: circleButtonSurface.height / 2 };

const rm703Text = '703';
const rm703TextRect = { x: rm703ButtonSurface.width / 2, y: rm703ButtonSurface.height / 2 };

const rm705Text = '705';
const rm705TextRect = { x: rm705ButtonSurface.width / 2, y: rm705ButtonSurface.height / 2 };

const rm704Text = '704';
const rm704TextRect = { x: rm704ButtonSurface.width / 2, y: rm704ButtonSurface.height / 2 };

const rm706Text = '706';
const rm706TextRect = { x: rm706ButtonSurface.width / 2, y: rm706ButtonSurface.height / 2 };

const rm707Text = '707';
const rm707TextRect = { x: rm707ButtonSurface.width / 2, y: rm707ButtonSurface.height / 2 };

const rm708Text = '708';
const rm708TextRect = { x: rm708ButtonSurface.width / 2, y: rm708ButtonSurface.height / 2 };

const rm709Text = '709';
const rm709TextRect = { x: rm709ButtonSurface.width / 2, y: rm709ButtonSurface.height / 2 };

const rm801Text = '801';
const rm801TextRect = { x: rm801ButtonSurface.width / 2, y: rm801ButtonSurface.height / 2 };

const rm802Text = '802';
const rm802TextRect = { x: rm802ButtonSurface.width / 2, y: rm802ButtonSurface.height / 2 };

const rr1Text = 'RR';
const rr1TextRect = { x: rr1ButtonSurface.width / 2, y: rr1ButtonSurface.height / 2 };

const weightText = 'Image';
const weightTextRect = { x: weightButtonSurface.width / 2, y: weightButtonSurface.height / 2 };
// Green 
// Yellow
const rm501Text = '501';
const rm501TextRect = { x: rm501ButtonSurface.width / 2, y: rm501ButtonSurface.height / 2 };

const rm502Text = '502';
const rm502TextRect = { x: rm502ButtonSurface.width / 2, y: rm502ButtonSurface.height / 2 };

const rm503Text = '503';
const rm503TextRect = { x: rm503ButtonSurface.width / 2, y: rm503ButtonSurface.height / 2 };

const rm504Text = '504';
const rm504TextRect = { x: rm504ButtonSurface.width / 2, y: rm504ButtonSurface.height / 2 };

const rm505Text = '505';
const rm505TextRect = { x: rm505ButtonSurface.width / 2, y: rm505ButtonSurface.height / 2 };

const rm506Text = '506';
const rm506TextRect = { x: rm506ButtonSurface.width / 2, y: rm506ButtonSurface.height / 2 };

const rm507Text = '507';
const rm507TextRect = { x: rm507ButtonSurface.width / 2, y: rm507ButtonSurface.height / 2 };

const rm508Text = '508';
const rm508TextRect = { x: rm508ButtonSurface.width / 2, y: rm508ButtonSurface.height / 2 };

const rm509Text = '509';
const rm509TextRect = { x: rm509ButtonSurface.width / 2, y: rm509ButtonSurface.height / 2 };

const rm510Text = '510';
const rm510TextRect = { x: rm510ButtonSurface.width / 2, y: rm510ButtonSurface.height / 2 };

const rm511Text = '511';
const rm511TextRect = { x: rm511ButtonSurface.width / 2, y: rm511ButtonSurface.height / 2 };

const rm512Text = '512';
const rm512TextRect = { x: rm512ButtonSurface.width / 2, y: rm512ButtonSurface.height / 2 };

const rm514Text = '514';
const rm514TextRect = { x: rm514ButtonSurface.width / 2, y: rm514ButtonSurface.height / 2 };

const rm515Text = '515';
const rm515TextRect = { x: rm515ButtonSurface.width / 2, y: rm515ButtonSurface.height / 2 };

const rm516Text = '516';
const rm516TextRect = { x: rm516ButtonSurface.width / 2, y: rm516ButtonSurface.height / 2 };

const rm517Text = '517';
const rm517TextRect = { x: rm517ButtonSurface.width / 2, y: rm517ButtonSurface.height / 2 };

const rrYellowText = 'RR';
const rrYellowTextRect = { x: rrYellowButtonSurface.width / 2, y: rrYellowButtonSurface.height / 2 };
// Yellow
// Blue
const rm905Text = '905';
const rm905TextRect = { x: rm905ButtonSurface.width / 2, y: rm905ButtonSurface.height / 2 };

const rm904Text = '904';
const rm904TextRect = { x: rm904ButtonSurface.width / 2, y: rm904ButtonSurface.height / 2 };

const tennisCourtsText = 'Tennis Courts';
const tennisCourtsTextRect = { x: tennisCourtsButtonSurface.width / 2, y: tennisCourtsButtonSurface.height / 2 };

const lemonParkingLotText = 'Lemon Parking Lot';
const lemonParkingLotTextRect = { x: lemonParkingLotButtonSurface.width / 2, y: lemonParkingLotButtonSurface.height / 2 };

const lawnText = 'Lawn';
const lawnTextRect = { x: lawnButtonSurface.width / 2, y: lawnButtonSurface.height / 2 };

const mediaCenterText = 'Media Center';
const mediaCenterTextRect = { x: mediaCenterButtonSurface.width / 2, y: mediaCenterButtonSurface.height / 2 };

const senateRoomText = 'Senate Room';
const senateRoomTextRect = { x: senateRoomButtonSurface.width / 2, y: senateRoomButtonSurface.height / 2 };

const mc1Text = 'MC1';
const mc1TextRect = { x: mc1ButtonSurface.width / 2, y: mc1ButtonSurface.height / 2 };

const mc2Text = 'MC2';
const mc2TextRect = { x: mc2ButtonSurface.width / 2, y: mc2ButtonSurface.height / 2 };

const mc3Text = 'MC3';
const mc3TextRect = { x: mc3ButtonSurface.width / 2, y: mc3ButtonSurface.height / 2 };

const mc4Text = 'MC4';
const mc4TextRect = { x: mc4ButtonSurface.width / 2, y: mc4ButtonSurface.height / 2 };
// Blue
// Orange
const poText = "Principal's Office";
const poTextRect = { x: poButtonSurface.width / 2, y: poButtonSurface.height / 2 };

const confText = 'Conf. Room';
const confTextRect = { x: confButtonSurface.width / 2, y: confButtonSurface.height / 2 };

const nurseText = 'Nurse';
const nurseTextRect = { x: nurseButtonSurface.width / 2, y: nurseButtonSurface.height / 2 };

const rgrText = 'Registrar';
const rgrTextRect = { x: rgrButtonSurface.width / 2, y: rgrButtonSurface.height / 2 };

const attendanceText = 'Attendance';
const attendanceTextRect = { x: attendanceButtonSurface.width / 2, y: attendanceButtonSurface.height / 2 };

const rm311Text = '311';
const rm311TextRect = { x: rm311ButtonSurface.width / 2, y: rm311ButtonSurface.height / 2 };

const rm310Text = '310';
const rm310TextRect = { x: rm310ButtonSurface.width / 2, y: rm310ButtonSurface.height / 2 };

const cccText = 'Counseling/College & Career';
const cccTextRect = { x: cccButtonSurface.width / 2, y: cccButtonSurface.height / 2 };

const rm304Text = '304';
const rm304TextRect = { x: rm304ButtonSurface.width / 2, y: rm304ButtonSurface.height / 2 };

const rrOrangeText = 'RR';
const rrOrangeTextRect = { x: rrOrangeButtonSurface.width / 2, y: rrOrangeButtonSurface.height / 2 };

const rm309Text = '309';
const rm309TextRect = { x: rm309ButtonSurface.width / 2, y: rm309ButtonSurface.height / 2 };

const rm308Text = '308';
const rm308TextRect = { x: rm308ButtonSurface.width / 2, y: rm308ButtonSurface.height / 2 };

const rm305Text = '305';
const rm305TextRect = { x: rm305ButtonSurface.width / 2, y: rm305ButtonSurface.height / 2 };

const rm306Text = '306';
const rm306TextRect = { x: rm306ButtonSurface.width / 2, y: rm306ButtonSurface.height / 2 };

const rm307Text = '307';
const rm307TextRect = { x: rm307ButtonSurface.width / 2, y: rm307ButtonSurface.height / 2 };

const lunchText = 'Lunch';
const lunchTextRect = { x: lunchButtonSurface.width / 2, y: lunchButtonSurface.height / 2 };
// Orange
// Brown
const poolButtonText = 'Pool';
const poolButtonTextRect = { x: poolButtonSurface.width / 2, y: poolButtonSurface.height / 2 };

const rm804ButtonText = '804';
const rm804ButtonTextRect = { x: rm804ButtonSurface.width / 2, y: rm804ButtonSurface.height / 2 };

const rm805ButtonText = '805';
const rm805ButtonTextRect = { x: rm805ButtonSurface.width / 2, y: rm805ButtonSurface.height / 2 };

const lockerRoomsButtonText = 'Locker';
const lockerRoomsButtonTextRect = { x: lockerRoomsButtonSurface.width / 2, y: lockerRoomsButtonSurface.height / 2 };

const rm207ButtonText = '207';
const rm207ButtonTextRect = { x: rm207ButtonSurface.width / 2, y: rm207ButtonSurface.height / 2 };

const rm206ButtonText = '206';
const rm206ButtonTextRect = { x: rm206ButtonSurface.width / 2, y: rm206ButtonSurface.height / 2 };

const rm205ButtonText = '205';
const rm205ButtonTextRect = { x: rm205ButtonSurface.width / 2, y: rm205ButtonSurface.height / 2 };

const rm204ButtonText = '204';
const rm204ButtonTextRect = { x: rm204ButtonSurface.width / 2, y: rm204ButtonSurface.height / 2 };

const rm203ButtonText = '203';
const rm203ButtonTextRect = { x: rm203ButtonSurface.width / 2, y: rm203ButtonSurface.height / 2 };

const rm202ButtonText = '202';
const rm202ButtonTextRect = { x: rm202ButtonSurface.width / 2, y: rm202ButtonSurface.height / 2 };

const rm201ButtonText = '201';
const rm201ButtonTextRect = { x: rm201ButtonSurface.width / 2, y: rm201ButtonSurface.height / 2 };

const rm107ButtonText = '107';
const rm107ButtonTextRect = { x: rm107ButtonSurface.width / 2, y: rm107ButtonSurface.height / 2 };

const rm106ButtonText = '106';
const rm106ButtonTextRect = { x: rm106ButtonSurface.width / 2, y: rm106ButtonSurface.height / 2 };

const rm105ButtonText = '105';
const rm105ButtonTextRect = { x: rm105ButtonSurface.width / 2, y: rm105ButtonSurface.height / 2 };

const rm104ButtonText = '104';
const rm104ButtonTextRect = { x: rm104ButtonSurface.width / 2, y: rm104ButtonSurface.height / 2 };

const rm103ButtonText = '103';
const rm103ButtonTextRect = { x: rm103ButtonSurface.width / 2, y: rm103ButtonSurface.height / 2 };

const rm102ButtonText = '102';
const rm102ButtonTextRect = { x: rm102ButtonSurface.width / 2, y: rm102ButtonSurface.height / 2 };

const rm101ButtonText = '101';
const rm101ButtonTextRect = { x: rm101ButtonSurface.width / 2, y: rm101ButtonSurface.height / 2 };
//Brown

// Back
const backButtonText = 'Back';
const backButtonRect = { x: backButtonSurface.width / 2, y: backButtonSurface.height / 2 };
// Back


// Create button boundaries
// Red
const rm601ButtonRect = { x: 775, y: 400, width: 50, height: 25 };
const staffLoungeButtonRect = { x: 743, y: 268, width: 115, height: 51 };
const rm216ButtonRect = { x: 847, y: 655, width: 50, height: 25 };
const rm215ButtonRect = { x: 904, y: 655, width: 50, height: 25 };
const rm214ButtonRect = { x: 960, y: 655, width: 50, height: 25 };
const RR1ButtonRect = { x: 1016, y: 655, width: 50, height: 25 };
const rm116ButtonRect = { x: 847, y: 690, width: 50, height: 25 };
const rm115ButtonRect = { x: 904, y: 690, width: 50, height: 25 };
const rm114ButtonRect = { x: 960, y: 690, width: 50, height: 25 };
const RR2ButtonRect = { x: 1015, y: 690, width: 50, height: 25 };
const rm213ButtonRect = { x: 1133, y: 655, width: 50, height: 25 };
const rm113ButtonRect = { x: 1133, y: 692, width: 50, height: 25 };
const rm108ButtonRect = { x: 1133, y: 773, width: 50, height: 25 };
const rm208ButtonRect = { x: 1133, y: 738, width: 50, height: 25 };
const rm212ButtonRect = { x: 795, y: 738, width: 50, height: 25 };
const rm211ButtonRect = { x: 852, y: 738, width: 50, height: 25 };
const rm210ButtonRect = { x: 908, y: 738, width: 50, height: 25 };
const rm209ButtonRect = { x: 963, y: 738, width: 50, height: 25 };
const RR3ButtonRect = { x: 1020, y: 738, width: 50, height: 25 };
const rm112ButtonRect = { x: 795, y: 773, width: 50, height: 25 };
const rm111ButtonRect = { x: 852, y: 773, width: 50, height: 25 };
const rm110ButtonRect = { x: 908, y: 773, width: 50, height: 25 };
const rm109ButtonRect = { x: 963, y: 773, width: 50, height: 25 };
const RR4ButtonRect = { x: 1020, y: 773, width: 50, height: 25 };
// Red
// Purple
const RR400ButtonRect = { x: 1018, y: 395, width: 36, height: 10 };
const rm401ButtonRect = { x: 1018, y: 410, width: 36, height: 44 };
const rm402ButtonRect = { x: 1018, y: 320, width: 36, height: 44 };
const rm403ButtonRect = { x: 1018, y: 265, width: 36, height: 44 };
const rm404ButtonRect = { x: 1018, y: 210, width: 36, height: 44 };
const rm405ButtonRect = { x: 1058, y: 210, width: 36, height: 44 };
const rm406ButtonRect = { x: 1058, y: 265, width: 36, height: 44 };
const rm407ButtonRect = { x: 1058, y: 320, width: 36, height: 44 };
const rm408ButtonRect = { x: 1058, y: 410, width: 36, height: 44 };
const rm409ButtonRect = { x: 1058, y: 467, width: 36, height: 44 };
const rm410ButtonRect = { x: 1018, y: 467, width: 35, height: 44 };
// Purple
// Green
const gymButtonRect = { x: 475, y: 414, width: 70, height: 50 };
const tennisButtonRect = { x: 441, y: 292, width: 39, height: 50 };
const rm702ButtonRect = { x: 499, y: 306, width: 50, height: 25 };
const circleButtonRect = { x: 645, y: 411, width: 49, height: 33 };
const rm703ButtonRect = { x: 560, y: 309, width: 48, height: 25 };
const rm705ButtonRect = { x: 639, y: 309, width: 23, height: 25 };
const rm704ButtonRect = { x: 611, y: 309, width: 23, height: 25 };
const rm706ButtonRect = { x: 666, y: 333, width: 22, height: 25 };
const rm707ButtonRect = { x: 666, y: 303, width: 22, height: 25 };
const rm708ButtonRect = { x: 666, y: 273, width: 22, height: 25 };
const rm801ButtonRect = { x: 572, y: 405, width: 22, height: 25 };
const rm802ButtonRect = { x: 572, y: 429, width: 22, height: 25 };
const rm709ButtonRect = { x: 638, y: 248, width: 25, height: 22 };
const rr1ButtonRect = { x: 666, y: 243, width: 21, height: 25 };
const weightButtonRect = { x: 505, y: 180, width: 30, height: 20 };
// Green
// Yellow
const rm501ButtonRect = { x: 1098, y: 429, width: 35, height: 25 };
const rm502ButtonRect = { x: 1097, y: 397, width: 37, height: 25 };
const rm503ButtonRect = { x: 1097.7, y: 345, width: 37, height: 25 };
const rm504ButtonRect = { x: 1097.7, y: 317, width: 37, height: 25 };
const rm505ButtonRect = { x: 1098.3, y: 284, width: 36, height: 25 };
const rm506ButtonRect = { x: 1097.5, y: 248, width: 35, height: 25 };
const rm507ButtonRect = { x: 1097.5, y: 210, width: 35, height: 25 };
const rm508ButtonRect = { x: 1137, y: 210, width: 38, height: 25 };
const rm509ButtonRect = { x: 1137, y: 248, width: 38.5, height: 25 };
const rm510ButtonRect = { x: 1137, y: 284, width: 35, height: 25 };
const rm511ButtonRect = { x: 1138, y: 317, width: 35, height: 25 };
const rm512ButtonRect = { x: 1137, y: 345.7, width: 35, height: 25 };
const rm514ButtonRect = { x: 1137, y: 397.5, width: 35, height: 25 };
const rm515ButtonRect = { x: 1137, y: 429, width: 35, height: 25 };
const rm516ButtonRect = { x: 1137, y: 478, width: 35, height: 25 };
const rm517ButtonRect = { x: 1098, y: 478, width: 35, height: 25 };
const RRYellowButtonRect = { x: 1098, y: 372, width: 35, height: 10.5 };
// Yellow
// Blue
const rm905ButtonRect = { x: 420, y: 561, width: 50, height: 25 };
const rm904ButtonRect = { x: 500, y: 561, width: 50, height: 25 };
const tennisCourtsButtonRect = { x: 162, y: 775, width: 120, height: 25 };
const lemonParkingLotButtonRect = { x: 290, y: 760, width: 124, height: 50 };
const lawnButtonRect = { x: 470, y: 750, width: 70, height: 35 };
const mediaCenterButtonRect = { x: 600, y: 805, width: 120, height: 25 };
const senateRoomButtonRect = { x: 643, y: 675, width: 80, height: 25 };
const mc1ButtonRect = { x: 600, y: 736, width: 40, height: 25 };
const mc2ButtonRect = { x: 600, y: 712, width: 40, height: 25 };
const mc3ButtonRect = { x: 600, y: 687, width: 40, height: 25 };
const mc4ButtonRect = { x: 600, y: 663, width: 40, height: 25 };
// Blue
// Orange
const POButtonRect = { x: 694, y: 545, width: 50, height: 25 };
const nurseButtonRect = { x: 779, y: 517, width: 50, height: 25 };
const rgrButtonRect = { x: 818, y: 517, width: 50, height: 25 };
const confButtonRect = { x: 694, y: 585, width: 50, height: 25 };
const attendanceButtonRect = { x: 876, y: 585, width: 50, height: 25 };
const rm311ButtonRect = { x: 876, y: 545, width: 50, height: 25 };
const rm310ButtonRect = { x: 960, y: 545, width: 50, height: 25 };
const cccButtonRect = { x: 923, y: 585, width: 80, height: 25 };
const rm304ButtonRect = { x: 1031, y: 590, width: 50, height: 25 };
const rrOrangeButtonRect = { x: 1062, y: 565, width: 16, height: 25 };
const rm309ButtonRect = { x: 1105, y: 551, width: 50, height: 25 };
const rm308ButtonRect = { x: 1152, y: 551, width: 50, height: 25 };
const rm305ButtonRect = { x: 1105, y: 590, width: 30, height: 25 };
const rm306ButtonRect = { x: 1143, y: 590, width: 25, height: 25 };
const rm307ButtonRect = { x: 1170, y: 590, width: 25, height: 25 };
const lunchButtonRect = { x: 910, y: 299, width: 70, height: 53 };
// Orange
// Brown
const poolButtonRect = { x: 775, y: 400, width: 50, height: 25 };
const rm804ButtonRect = { x: 385, y: 415, width: 50, height: 25 };
const rm805ButtonRect = { x: 385, y: 485, width: 50, height: 25 };
const lockerRoomsButtonRect = { x: 385, y: 450, width: 50, height: 25 };
const rm207ButtonRect = { x: 795, y: 820, width: 50, height: 25 };
const rm206ButtonRect = { x: 850, y: 820, width: 50, height: 25 };
const rm205ButtonRect = { x: 905, y: 820, width: 50, height: 25 };
const rm204ButtonRect = { x: 963, y: 820, width: 50, height: 25 };
const rm203ButtonRect = { x: 1018, y: 820, width: 50, height: 25 };
const rm202ButtonRect = { x: 1072, y: 820, width: 50, height: 25 };
const rm201ButtonRect = { x: 1130, y: 820, width: 50, height: 25 };
const rm107ButtonRect = { x: 795, y: 857, width: 50, height: 25 };
const rm106ButtonRect = { x: 850, y: 857, width: 50, height: 25 };
const rm105ButtonRect = { x: 905, y: 857, width: 50, height: 25 };
const rm104ButtonRect = { x: 963, y: 857, width: 50, height: 25 };
const rm103ButtonRect = { x: 1018, y: 857, width: 50, height: 25 };
const rm102ButtonRect = { x: 1072, y: 857, width: 50, height: 25 };
const rm101ButtonRect = { x: 1130, y: 857, width: 50, height: 25 };
// Brown
// Back
const backButtonRectBoundary = { x: 30, y: 20, width: 100, height: 50 };
// Back

// Create button hover effect function
function buttonHoverEffect(buttonRect, buttonSurface) {
    const mouseX = event.clientX;
    const mouseY = event.clientY;
    if (mouseX >= buttonRect.x && mouseX <= buttonRect.x + buttonRect.width &&
        mouseY >= buttonRect.y && mouseY <= buttonRect.y + buttonRect.height) {
        context.fillStyle = 'rgba(127, 255, 212, 1)';
        context.fillRect(buttonRect.x, buttonRect.y, buttonRect.width, buttonRect.height);
    } else {
        context.fillStyle = 'white';
        context.fillRect(buttonRect.x, buttonRect.y, buttonRect.width, buttonRect.height);
    }
}

// Start the main loop
function mainLoop() {
    // Set the frame rate
    clock.tick(60);

    // Fill the display with color
    context.fillStyle = 'rgba(155, 255, 155, 1)';
    context.fillRect(0, 0, canvas.width, canvas.height);

    // Get events from the event queue
    window.addEventListener('click', function (event) {
        // Check for the mouse button down event
        if (event.button === 0) {
            // Red
            if (mouseX >= rm601ButtonRect.x && mouseX <= rm601ButtonRect.x + rm601ButtonRect.width &&
                mouseY >= rm601ButtonRect.y && mouseY <= rm601ButtonRect.y + rm601ButtonRect.height) {
                currentScreen = rm601Image;
            } else if (mouseX >= staffLoungeButtonRect.x && mouseX <= staffLoungeButtonRect.x + staffLoungeButtonRect.width &&
                mouseY >= staffLoungeButtonRect.y && mouseY <= staffLoungeButtonRect.y + staffLoungeButtonRect.height) {
                currentScreen = staffLoungeImage;
            } else if (mouseX >= backButtonRectBoundary.x && mouseX <= backButtonRectBoundary.x + backButtonRectBoundary.width &&
                mouseY >= backButtonRectBoundary.y && mouseY <= backButtonRectBoundary.y + backButtonRectBoundary.height) {
                currentScreen = mapImage;
            }
        }
    });

    // Check if the mouse is over the button. This will create the button hover effect
    // Red
    buttonHoverEffect(rm601ButtonRect, rm601ButtonSurface);
    buttonHoverEffect(staffLoungeButtonRect, staffLoungeButtonSurface);

    // Back
    buttonHoverEffect(backButtonRectBoundary, backButtonSurface);
    // Back

    // Draw the map and button on the screen
    if (currentScreen === mapImage) {
        context.drawImage(currentScreen, 0, 0);  // controls test_surface location
        // Red
        context.fillText(rm601Text, rm601ButtonRect.x + rm601TextRect.x, rm601ButtonRect.y + rm601TextRect.y);
        context.fillText(staffLoungeText, staffLoungeButtonRect.x + staffLoungeTextRect.x, staffLoungeButtonRect.y + staffLoungeTextRect.y);
    } else {
        context.drawImage(currentScreen, 0, 0);
        // Back
        context.fillText(backButtonText, backButtonRectBoundary.x + backButtonRect.x, backButtonRectBoundary.y + backButtonRect.y);
        // Back
    }

    // Update the game state
    requestAnimationFrame(mainLoop);
}

mainLoop();
