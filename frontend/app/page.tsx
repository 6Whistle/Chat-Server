'use client'
import { useState } from "react";
import axios from "axios";
import { SubmitHandler, useForm } from "react-hook-form";

type ChatForms = {
  response: string,
  question: string,
  category: string,
};

export default function Home() {
  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors },
  } = useForm<ChatForms>()

  const onSubmit: SubmitHandler<ChatForms> = ({question, category}) => 
    axios.post(`http://localhost:8000/chat/${category.replace(' ', '-').toLowerCase()}`, {question})
    .then((res) => setValue("response", res.data.answer))
    .catch((error) => setValue("response", JSON.stringify(error)))

  return (
<div className="w-full h-full bg-white flex-col justify-center items-center inline-flex">
<nav className="w-full h-16 px-20 py-3 bg-white shadow border-b border-neutral-200 justify-center items-start gap-[579px] inline-flex">
  <div className="text-black text-xl font-semibold font-['Inter'] leading-[30px]">6Whistle</div>
  <div className="w-[151px] justify-center items-center gap-8 flex">
    <div className="text-black text-base font-medium font-['Inter'] leading-normal">Tab</div>
    <div className="text-black text-base font-medium font-['Inter'] leading-normal">Tab</div>
    <div className="text-black text-base font-medium font-['Inter'] leading-normal">Tab</div>
  </div>
  <div className="justify-start items-start gap-3 flex">
    <div className="w-14 px-4 bg-zinc-100 rounded-lg justify-center items-center gap-2 flex">
      <div className="w-6 px-1 justify-center items-start gap-[5px] flex"></div>
    </div>
    <div className="w-24 px-4 bg-black rounded-lg justify-center items-center gap-2 flex">
      <div className="text-white text-base font-medium font-['Inter'] leading-normal">Register</div>
    </div>
  </div>
</nav>
  <form onSubmit={handleSubmit(onSubmit)} className="w-full h-full p-6 bg-white flex-col justify-center items-center gap-8 flex">
    <div className="w-[1200px] h-[500px] flex-col justify-start items-start gap-6 flex">
      <div className="self-stretch text-black text-[64px] font-bold font-['Inter']">BIT-LLM</div>
      <div className="self-stretch text-zinc-500 text-2xl font-normal font-['Inter'] leading-9">Ask all to BIT-LLM</div>
      <div className="self-stretch text-black text-xl font-medium font-['Inter'] leading-[30px]">{watch("response")}</div>
    </div>

    <div className="w-[255px] h-14 p-2 bg-neutral-100 rounded-xl justify-center items-start gap-2 inline-flex">
  {
  watch("category") === "Titanic" ? 
  <div className="px-4 py-2 bg-white rounded-lg justify-center items-center gap-2 flex">
    <div className="text-black text-base font-medium font-['Inter'] leading-normal">Titanic</div>
  </div> : 
  <div className="px-4 py-2 bg-neutral-100 rounded-lg justify-center items-center gap-2 flex">
    <input type="submit" onClick={() => setValue("category", "Titanic")} value="Titanic" className="text-black text-base font-medium font-['Inter'] leading-normal" />
  </div>
}
{
  watch("category") === "AI" ? 
  <div className="px-4 py-2 bg-white rounded-lg justify-center items-center gap-2 flex">
    <div className="text-black text-base font-medium font-['Inter'] leading-normal">AI</div>
  </div> : 
  <div className="px-4 py-2 bg-neutral-100 rounded-lg justify-center items-center gap-2 flex">
    <input type="submit" onClick={() => setValue("category", "AI")}  value="AI" className="text-black text-base font-medium font-['Inter'] leading-normal" />
  </div>
}
{
  watch("category") === "Tab 2" ? 
  <div className="px-4 py-2 bg-white rounded-lg justify-center items-center gap-2 flex">
    <div className="text-black text-base font-medium font-['Inter'] leading-normal">Tab 2</div>
  </div> : 
  <div className="px-4 py-2 bg-neutral-100 rounded-lg justify-center items-center gap-2 flex">
    <input type="submit" onClick={() => setValue("category", "Tab 2")} value="Tab 2" className="text-black text-base font-medium font-['Inter'] leading-normal" />
  </div>
}
</div>
    <div className="w-[1213px] h-10 px-4 py-2 bg-white rounded-lg border border-neutral-200 justify-start items-center gap-4 inline-flex">
      <input type="text" {...register("question", { required: true })} className="w-[987px] h-7 text-zinc-500 text-base font-normal font-['Inter'] leading-normal" />
      <div className="w-6 h-6 relative"></div>
      <div className="w-6 h-6 relative"></div>
      <div className="w-6 h-6 relative"></div>
      <div className="w-[66px] h-8 px-6 py-3.5 bg-black rounded-lg shadow justify-center items-center gap-2 flex">
        <button type="submit" className="text-white text-base font-medium font-['Inter'] leading-normal">Send</button>
      </div>
    </div>
  </form>
</div>
  )
}
