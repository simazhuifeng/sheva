

import static org.quartz.CronScheduleBuilder.cronSchedule;
import static org.quartz.JobBuilder.newJob;
import static org.quartz.TriggerBuilder.newTrigger;

import java.util.Date;

import org.nutz.dao.Dao;
import org.nutz.log.Log;
import org.nutz.log.Logs;
import org.nutz.mvc.NutConfig;
import org.nutz.mvc.Setup;
import org.quartz.JobDataMap;
import org.quartz.JobDetail;
import org.quartz.Scheduler;
import org.quartz.SchedulerException;
import org.quartz.Trigger;

import service.WeizhangService;
import utils.ProxyCheckTask;

public class AppSetup implements Setup {

	private static final Log log = Logs.get();
	Scheduler scheduler;

	public void destroy(NutConfig config) {
		if (scheduler != null) {
			try {
				log.info("scheduler shutdown ....");
				scheduler.shutdown(true);
			} catch (SchedulerException e) {
				log.error("scheduler shutdown failed.", e);
			} finally {

			}
		}

	}

	public void init(NutConfig config) {

		Dao dao = config.getIoc().get(Dao.class);
		WeizhangService ws = config.getIoc().get(WeizhangService.class);

		Date runTime = new Date();

		JobDataMap map = new JobDataMap();
		map.put("WeizhangService", ws);

		try {
			JobDetail job = newJob(ProxyCheckTask.class)
					.withIdentity("ProxyCheckTask", "group1").usingJobData(map).build();
			// Trigger the job to run on the next round minute
			Trigger trigger = newTrigger().withIdentity("trigger1", "group1")
					.startAt(runTime)
					.withSchedule(cronSchedule("0 0/2 * * * ?")).build();
			
			// Tell quartz to schedule the job using our trigger
			scheduler.scheduleJob(job, trigger);
			scheduler.start();
		} catch (SchedulerException e) {
			log.error("Scheduler start failed.", e);
		}
	}

}