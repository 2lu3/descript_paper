import type { Route } from "./+types/home";
import { Form, redirect } from "react-router";
import { env } from "~/utils/env.server";

export function meta({ }: Route.MetaArgs) {
  return [
    { title: "New React Router App" },
    { name: "description", content: "Welcome to React Router!" },
  ];
}

export async function action({ request }: Route.ActionArgs) {
  let formData = await request.formData();
  let file = formData.get("file");
  if (!(file instanceof File)) {
    throw new Response("File is required", { status: 400 });
  }

  const postResponse = await fetch(`${env.BACKEND_API_BASE_URL}/uploads`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      filename: file.name,
      size: file.size,
      content_type: file.type,
    }),
  });

  if (!postResponse.ok) {
    throw new Response("Failed to upload file", { status: postResponse.status });
  }
  const uploadParam = await postResponse.json();
  const uploadUrl = uploadParam.url;
  const uploadKey = uploadParam.key;

  const uploadResponse = await fetch(uploadUrl, {
    method: "PUT",
    headers: { "Content-Type": file.type },
    body: file,
  });
  if (!uploadResponse.ok) {
    throw new Response("Failed to upload file", { status: uploadResponse.status });
  }
  return redirect(`/progress/${uploadKey}`);
}

export default function Home() {
  return (
    <div className="grid min-h-screen place-items-center prose">
      <h1>Drop your PDF file here</h1>
      <Form method="post" encType="multipart/form-data">
        <input type="file" name="file" className="file-input" />
        <button type="submit" className="btn">送信</button>
      </Form>
    </div>
  );
}
