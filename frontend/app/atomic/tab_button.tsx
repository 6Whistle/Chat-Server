export default function TabButton(tabName: string) {
  return (
    <div className="text-black text-base font-medium font-['Inter'] leading-normal">
      {tabName}
    </div>
  );
}

export const tabNames: string[] = [
  "Tab",
  "Tab",
  "Tab",
];