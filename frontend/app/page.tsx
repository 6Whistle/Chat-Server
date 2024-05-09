'use client'
import { useState } from "react";
import axios from "axios";
import { SubmitHandler, useForm } from "react-hook-form";

type ChatForms = {
  response: string,
  question: string
};

export default function Home() {
  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors },
  } = useForm<ChatForms>()

  const onSubmit: SubmitHandler<ChatForms> = (data) => 
    axios.post("http://localhost:8000/chat", data)
    .then((res) => setValue("response", res.data.answer))
    .catch((error) => setValue("response", JSON.stringify(error)))

  return (
    <div className="flex h-screen justify-center items-center">
      <div className="w-full max-w-md">
      <form onSubmit={handleSubmit(onSubmit)}>
        <h2 className="text-3xl font-bold mb-6">6Whistle's Chat GPT</h2>
        <div className="bg-gray-100 rounded-lg p-6 mb-6">
          <div className="h-64 overflow-y-auto">
            {watch("response")}
          </div>
        </div>
          <input type="text" {...register("question", { required: true })} className="w-full mb-4 p-3 border border-gray-300 rounded" />
          <button type="submit" className="w-full py-3 bg-blue-500 text-white font-bold rounded">전송</button>
        </form>
        {errors.question && <span>This field is required</span>}
      </div>
    </div>
  );
}
