"use client";
import axios from "axios";
import {
  SubmitErrorHandler,
  SubmitHandler,
  set,
  useForm,
} from "react-hook-form";
import ImageButton, { buttonImagesUrl } from "./atomic/image_button";
import TextInput from "./atomic/text_input";
import { url } from "inspector";
import Header from "./component/header";

type ChatForms = {
  response: string;
  question: string;
  category: string;
};

export default function Home() {
  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors },
  } = useForm<ChatForms>();

  const onSubmit: SubmitHandler<ChatForms> = ({ question, category }) => {
    if (!category) {
      setValue("response", "Please choose a category");
      return;
    }
    setValue("response", "Loading...");
    axios
      .post(
        `http://localhost:8000/chat/${category
          .replace(" ", "-")
          .toLowerCase()}`,
        { question }
      )
      .then((res) => setValue("response", res.data.answer))
      .catch((error) => setValue("response", JSON.stringify(error)));
  };

  const onInValid: SubmitErrorHandler<ChatForms> = ({ question }) => {
    setValue("response", "Please enter a question");
  };

  return (
    <div className="w-full h-full bg-white flex-col justify-center items-center flex">
      {Header()}
      <form
        onSubmit={handleSubmit(onSubmit, onInValid)}
        className="w-full h-full p-6 bg-white flex-col justify-center items-center gap-8 flex"
      >
        <div className="w-5/6 h-[500px] px-10 py-5 flex-col bg-zinc-100 justify-start items-start gap-6 flex rounded-lg">
          <div className="self-stretch text-black text-[64px] font-bold font-['Inter']">
            BIT-LLM
          </div>
          <div className="self-stretch text-zinc-500 text-2xl font-normal font-['Inter'] leading-9">
            Ask everything to BIT-LLM
          </div>
          <div className="self-stretch text-black text-xl font-medium font-['Inter'] leading-[30px]">
            {watch("response")}
          </div>
        </div>

        <div className="w-[255px] h-14 p-2 bg-neutral-100 rounded-xl justify-center items-start gap-2 inline-flex">
          {watch("category") === "Titanic" ? (
            <div className="px-4 py-2 bg-white rounded-lg justify-center items-center gap-2 flex">
              <div className="text-black text-base font-medium font-['Inter'] leading-normal">
                Titanic
              </div>
            </div>
          ) : (
            <div className="px-4 py-2 bg-neutral-100 rounded-lg justify-center items-center gap-2 flex">
              <input
                type="submit"
                onClick={() => setValue("category", "Titanic")}
                value="Titanic"
                className="text-black text-base font-medium font-['Inter'] leading-normal"
              />
            </div>
          )}
          {watch("category") === "AI" ? (
            <div className="px-4 py-2 bg-white rounded-lg justify-center items-center gap-2 flex">
              <div className="text-black text-base font-medium font-['Inter'] leading-normal">
                AI
              </div>
            </div>
          ) : (
            <div className="px-4 py-2 bg-neutral-100 rounded-lg justify-center items-center gap-2 flex">
              <input
                type="submit"
                onClick={() => setValue("category", "AI")}
                value="AI"
                className="text-black text-base font-medium font-['Inter'] leading-normal"
              />
            </div>
          )}
          {watch("category") === "Tab 2" ? (
            <div className="px-4 py-2 bg-white rounded-lg justify-center items-center gap-2 flex">
              <div className="text-black text-base font-medium font-['Inter'] leading-normal">
                Tab 2
              </div>
            </div>
          ) : (
            <div className="px-4 py-2 bg-neutral-100 rounded-lg justify-center items-center gap-2 flex">
              <input
                type="submit"
                onClick={() => setValue("category", "Tab 2")}
                value="Tab 2"
                className="text-black text-base font-medium font-['Inter'] leading-normal"
              />
            </div>
          )}
        </div>
        <div className="w-5/6 h-10 px-4 py-2 bg-white rounded-lg border border-neutral-200 justify-start items-center gap-3 flex">
          {TextInput(register, "question")}
          {buttonImagesUrl.map((url) => ImageButton(url))}
          <div className="w-[60px] h-8 px-6 py-3.5 bg-black rounded-lg shadow justify-center items-center gap-2 flex">
            <button
              type="submit"
              className="text-white text-base font-medium font-['Inter'] leading-normal"
            >
              Send
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
