import HeaderButton from "../atomic/header/header_button";
import TabButton, { tabNames } from "../atomic/header/tab_button";

export default function Header() {
  return (
    <nav className="w-full h-16 px-20 py-4 bg-white shadow border-b border-neutral-200 justify-start items-center flex">
      <div className="text-black text-xl font-semibold font-['Inter'] leading-[30px] whitespace-nowrap">
        6Whistle Blog
      </div>
      <div className="w-full justify-center items-center gap-8 flex">
        {tabNames.map((tabName) => (
          <TabButton tabName={tabName} key={tabName} />
        ))}
      </div>
      <div className="justify-start items-start gap-3 flex">
        <div className="w-9 justify-center items-center gap-2 flex">
          <img src="/profile.svg" alt="profileImg" />
        </div>
        <HeaderButton text="Register" />
      </div>
    </nav>
  );
}
