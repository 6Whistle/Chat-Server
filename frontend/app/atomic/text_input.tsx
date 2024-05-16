import { UseFormRegister } from "react-hook-form";

export default function TextInput(
  register: UseFormRegister<any>,
  name: string
) {
  return (
    <input
      type="text"
      {...register(name, { required: true })}
      className="w-full h-7 text-zinc-500 text-base font-normal font-['Inter'] leading-normal"
    />
  );
}
