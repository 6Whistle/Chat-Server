export default function ImageButton({url}: {url:string}) {
  return <img src={url} id={url} className="w-7 h-7 relative" />;
}

export const buttonImagesUrl: string[] = [
  "/camera.svg",
  "/files.svg",
  "/position.svg",
];
