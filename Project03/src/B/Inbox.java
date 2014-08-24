package B;

import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;

public class Inbox {

	HashMap<Integer,String> messages = new HashMap<Integer, String>();
	Integer key = 0;
	
	public String getAll(){
		String inbox = "LIST";
		Iterator<Entry<Integer, String>> it = messages.entrySet().iterator();
	    while (it.hasNext()) {
	        Map.Entry<Integer, String> pairs = (Map.Entry<Integer, String>)it.next();
	        inbox = inbox + "\n" + pairs.getKey() + " = " + pairs.getValue();
	    }
	    return inbox+"\nEND";
	}
	
	public void add(String value){
		messages.put(key, value);
		key++;
	}
	
	public String remove(Integer k){
		return messages.remove(k);
	}
}
