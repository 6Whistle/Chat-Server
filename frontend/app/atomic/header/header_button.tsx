export default function HeaderButton({text} : {text: string}) {
  return (
    <button className="w-24 px-4 bg-black rounded-lg justify-center items-center gap-2 flex">
      <p className="text-white text-base font-medium font-['Inter'] leading-[35px]">
        {text}
      </p>
    </button>
  );
}