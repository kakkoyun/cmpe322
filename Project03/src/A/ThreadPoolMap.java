package A;

public class ThreadPoolMap {
	public static void main(String[] args) {
		if (args.length<1) {
			System.out.println("USAGE: ");
			System.out.println("ThreadPoolMap [CLIENT servername port] | [SERVER port]");
			System.exit(0);
		}
		if (args[0].equals("CLIENT")) {
			new Client(args[1], Integer.parseInt(args[2])).run();
		}
		else {
			new Server(Integer.parseInt(args[1])).run();
		}
	}
}
