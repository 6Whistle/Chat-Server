export default function ChatOutput({ title, subtitle, text }: { title: string, subtitle:string, text: string }) {
  return (
    <div className="w-5/6 h-[500px] px-10 py-5 flex-col bg-zinc-100 justify-start items-start gap-6 flex rounded-lg">
          <div className="self-stretch text-black text-[64px] font-bold font-['Inter']">
            {title}
          </div>
          <div className="self-stretch text-zinc-500 text-2xl font-normal font-['Inter'] leading-9">
            {subtitle}
          </div>
          <div className="self-stretch text-black text-xl font-medium font-['Inter'] leading-[30px]">
            {text}
          </div>
        </div>
  );
}