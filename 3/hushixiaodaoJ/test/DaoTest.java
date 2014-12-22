import org.junit.Test;
import org.nutz.dao.Dao;
import org.nutz.ioc.Ioc;
import org.nutz.ioc.impl.NutIoc;
import org.nutz.ioc.loader.json.JsonLoader;

import beans.Answer;
import beans.Ask;
import beans.Conversation;
import beans.Topic;
import beans.weizhang.PlateNumber;

public class DaoTest {
	@Test
	public void createTables(){
		Ioc ioc = new NutIoc(new JsonLoader("ioc/config.js"));
		Dao dao = ioc.get(Dao.class);
		if(!dao.exists(Conversation.class)){
			dao.create(Ask.class, false);
			dao.create(Answer.class, false);
			dao.create(PlateNumber.class, false);
			dao.create(Topic.class, false);
		}
	}
}
