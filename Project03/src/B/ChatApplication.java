package B;


public class ChatApplication {
	public static void main(String[] args) {
		if (args.length<1) {
			System.out.println("USAGE: ");
			System.out.println("ClientApplication [CLIENT servername port nickname] | [SERVER port]");
			System.exit(0);
		}
		if (args[0].equals("CLIENT")) {
			new Client(args[1], Integer.parseInt(args[2]), args[3]).run();
		}
		else {
			new Server(Integer.parseInt(args[1])).run();
		}
	}
}
