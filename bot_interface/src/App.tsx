import { ChangeEvent, useEffect, useRef, useState } from "react";

export default function App() {
	interface Message {
		[key: string]: string;
	}
	const [inputValue, setInputValue] = useState<string>("");
	const [messages, setMessages] = useState<Message[]>([]);
	const onChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
		setInputValue(e.target.value);
	};
	const onSubmit = async () => {
		try {
			const response = await fetch("http://127.0.0.1:5000", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ text: inputValue }),
			});

			if (response.ok) {
				console.log("Input sent");
			} else console.log("Failed to send input");

			response.json().then((data) => {
				data = data.response;
				const newMsg: Message = { [inputValue]: data };
				const newMessages = [...messages, newMsg];
				setMessages(newMessages);
				setInputValue("");
			});
		} catch (error) {
			console.log("Error: ", error);
		}
	};
	const msgRef = useRef<HTMLDivElement>(null);
	useEffect(() => {
		if (msgRef.current){
			msgRef.current.scrollIntoView({behavior: "smooth"});
		}
	}, [messages]);

	return (
		<>
			<div className="head-div flex justify-center items-center px-3 sticky top-0">
				<p className="head">utp.ai</p>
				{/* <div className="button-1 flex">
					<button className="mx-3 px-5 py-2">Login</button>
					<button className="mx-3 px-5 py-2">Sign Up</button>
				</div> */}
			</div>
			<div className="w-full h-full p-5">
				<div className="messages-view p-10 overscroll-contain overflow-y-auto">
					{messages.map((msg, ind) => {
						return (
							<div className="my-5" key={ind}>
								{Object.entries(msg).map(([key, value]) => (
									<div key={key} className="flex flex-col">
										<div className="flex flex-col items-end my-2">
											<div className="msg text-start w-9/12 rounded-2xl">{key}</div>
										</div>
										<div className="flex flex-col items-start my-2">
											<div className="msg text-start w-9/12 rounded-2xl">{value}</div>
										</div>
									</div>
								))}
							</div>
						);
					})}
					<div ref={msgRef}></div>
				</div>
				<div className="textbox rounded-lg flex justify-around items-center fixed bottom-0">
					<textarea
						className="w-10/12 text-white leading-tight rounded-xl"
						id="input"
						value={inputValue}
						onChange={onChange}
					/>
					<button
						type="submit"
						className="w-1/12 bg-zinc-800 text-white font-semibold rounded-lg p-3"
						onClick={onSubmit}
					>
						Go
					</button>
				</div>
			</div>
		</>
	);
}
