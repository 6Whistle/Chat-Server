import { UseFormRegister } from "react-hook-form";
import TextInput from "../atomic/chat/text_input";
import ImageButton, { buttonImagesUrl } from "../atomic/chat/image_button";

export default function ChatInput({
  register,
  targetText,
}: {
  register: UseFormRegister<any>;
  targetText: string;
}) {
  return (
    <div className="w-5/6 h-10 px-4 py-2 bg-white rounded-lg border border-neutral-200 justify-start items-center gap-3 flex">
      <TextInput register={register} target={targetText} />
      {buttonImagesUrl.map((url, i) => (
        <ImageButton key={i} url={url} />
      ))}
      <div className="w-[60px] h-8 px-6 py-3.5 bg-black rounded-lg shadow justify-center items-center gap-2 flex">
        <button
          type="submit"
          className="text-white text-base font-medium font-['Inter'] leading-normal"
        >
          Send
        </button>
      </div>
    </div>
  );
}
