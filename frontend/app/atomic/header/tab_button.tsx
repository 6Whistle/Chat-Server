export const TabButton = ({tabName}:{tabName:string}) => (
    <div
    className="text-black text-base font-medium font-['Inter'] leading-normal whitespace-nowrap">
      {tabName}
    </div>
  );

export const tabNames: string[] = [
  "Tab 1",
  "Tab 2",
  "Tab 3",
];

export default TabButton;