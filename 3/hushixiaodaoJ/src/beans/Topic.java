package beans;

import java.util.List;

import org.nutz.dao.entity.annotation.Column;
import org.nutz.dao.entity.annotation.Id;
import org.nutz.dao.entity.annotation.Many;
import org.nutz.dao.entity.annotation.Table;
@Table("t_topic")
public class Topic {
	@Column
	@Id
	private long topicId;
	@Column
	private String name;
	
	@Column("_group")
	private String group;
	
	@Many(target = Ask.class, field = "topicId")
	private List<Ask> asks;

	public long getTopicId() {
		return topicId;
	}
	public void setTopicId(long topicId) {
		this.topicId = topicId;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public String getGroup() {
		return group;
	}
	public void setGroup(String group) {
		this.group = group;
	}
	public List<Ask> getAsks() {
		return asks;
	}
	public void setAsks(List<Ask> asks) {
		this.asks = asks;
	}

}
