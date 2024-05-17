export default function TabButton({ tabName }: { tabName: string }) {
  return (
    <div className="text-black text-base font-medium font-['Inter'] leading-normal whitespace-nowrap">
      {tabName}
    </div>
  );
}

export const tabNames: string[] = ["Tab 1", "Tab 2", "Tab 3"];
