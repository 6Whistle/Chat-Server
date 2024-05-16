export default function ImageButton(url: string) {
  return <img src={url} className="w-7 h-7 relative" />;
}

export const buttonImagesUrl: string[] = [
  "/camera.png",
  "/word.png",
  "/position.png",
];
