import TabButton, { tabNames } from "../atomic/tab_button";

export default function Header() {
  return (
    <nav className="w-full h-16 px-20 py-4 bg-white shadow border-b border-neutral-200 justify-start items-center flex">
      <div className="text-black text-xl font-semibold font-['Inter'] leading-[30px]">
        6Whistle
      </div>
      <div className="w-full justify-center items-center gap-8 flex">
        {tabNames.map((tabName) => TabButton(tabName))}
        {/* <div className="text-black text-base font-medium font-['Inter'] leading-normal">
          Tab
        </div>
        <div className="text-black text-base font-medium font-['Inter'] leading-normal">
          Tab
        </div> */}
      </div>
      <div className="justify-start items-start gap-3 flex">
        <div className="w-14 px-4 bg-zinc-100 rounded-lg justify-center items-center gap-2 flex">
          <div className="w-6 px-1 justify-center items-start gap-[5px] flex"></div>
        </div>
        <div className="w-24 px-4 bg-black rounded-lg justify-center items-center gap-2 flex">
          <div className="text-white text-base font-medium font-['Inter'] leading-[35px]">
            Register
          </div>
        </div>
      </div>
    </nav>
  );
}
