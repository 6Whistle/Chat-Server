"use client";
import axios from "axios";
import {
  SubmitErrorHandler,
  SubmitHandler,
  set,
  useForm,
} from "react-hook-form";
import Header from "./component/header";
import RadioButton, { radioButtonList } from "./atomic/chat/radio_button";
import ChatInput from "./component/chat_input";
import ChatOutput from "./component/chat_output";

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

  const onInValid: SubmitErrorHandler<ChatForms> = () => {
    setValue("response", "Please enter a question");
  };

  return (
    <div className="w-full h-full bg-white flex-col justify-center items-center flex">
      <Header />
      <form
        onSubmit={handleSubmit(onSubmit, onInValid)}
        className="w-full h-full p-6 bg-white flex-col justify-center items-center gap-8 flex"
      >
        <ChatOutput
          title="BIT-LLM"
          subtitle="Ask everything to BIT-LLM"
          text={watch("response")}
        />
        <ul className="w-5/6 grid gap-6 md:grid-cols-3">
          {radioButtonList.map((radioButton, i) => (
            <RadioButton
              key={i}
              title={radioButton.title}
              subtitle={radioButton.subtitle}
              value={radioButton.value}
              target={radioButton.target}
              setValue={setValue}
            />
          ))}
        </ul>
        <ChatInput register={register} targetText="question" />
      </form>
    </div>
  );
}
