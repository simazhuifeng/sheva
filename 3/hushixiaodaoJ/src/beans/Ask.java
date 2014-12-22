package beans;

import org.nutz.dao.entity.annotation.Column;
import org.nutz.dao.entity.annotation.Id;
import org.nutz.dao.entity.annotation.Table;
@Table("t_ask")
public class Ask {
	@Column
	@Id
	private long askId;
	@Column
	private long topicId;
	@Column
	private String question;
	public long getAskId() {
		return askId;
	}
	public void setAskId(long askId) {
		this.askId = askId;
	}
	public long getTopicId() {
		return topicId;
	}
	public void setTopicId(long topicId) {
		this.topicId = topicId;
	}
	public String getQuestion() {
		return question;
	}
	public void setQuestion(String question) {
		this.question = question;
	}
}
