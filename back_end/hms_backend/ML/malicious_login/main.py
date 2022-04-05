import string
import pickle

my_model = pickle.load(open('maliciousLogin_model.pkl', 'rb'))


class MaliciousLogin():
    def __init__(self, model=my_model):
        self.model = model

    def get_predict(self, login_data):
        # duration: real
        # protocol_type: string
        # service: string
        # flag: string
        # src_bytes: real
        # dst_bytes: real
        # land: int
        # wrong_fragment: real
        # urgent: real
        # hot: real
        # num_failed_logins: real
        # logged_in: int
        # num_compromised: real
        # root_shell: real
        # su_attempted: real
        # num_root: real
        # num_file_creations: real
        # num_shells: real
        # num_access_files: real
        # num_outbound_cmds: real
        # is_host_login: int
        # is_guest_login: int
        # count: real
        # srv_count: real
        # serror_rate: real
        # srv_serror_rate: real
        # rerror_rate: real
        # srv_rerror_rate: real
        # same_srv_rate: real
        # diff_srv_rate: real
        # srv_diff_host_rate: real
        # dst_host_count: real
        # dst_host_srv_count: real
        # dst_host_same_srv_rate: real
        # dst_host_diff_srv_rate: real
        # dst_host_same_src_port_rate: real
        # dst_host_srv_diff_host_rate: real
        # dst_host_serror_rate: real
        # dst_host_srv_serror_rate: real
        # dst_host_rerror_rate: real
        # dst_host_srv_rerror_rate: real

        sample = [[login_data.duration,
                   login_data.protocol_type,
                   login_data.service,
                   login_data.flag,
                   login_data.src_bytes,
                   login_data.dst_bytes,
                   login_data.land,
                   login_data.wrong_fragment,
                   login_data.urgent,
                   login_data.hot,
                   login_data.num_failed_logins,
                   login_data.logged_in,
                   login_data.num_compromised,
                   login_data.root_shell,
                   login_data.su_attempted,
                   login_data.num_root,
                   login_data.num_file_creations,
                   login_data.num_shells,
                   login_data.num_access_files,
                   login_data.num_outbound_cmds,
                   login_data.is_host_login,
                   login_data.is_guest_login,
                   login_data.count,
                   login_data.srv_count,
                   login_data.serror_rate,
                   login_data.srv_serror_rate,
                   login_data.rerror_rate,
                   login_data.srv_rerror_rate,
                   login_data.same_srv_rate,
                   login_data.diff_srv_rate,
                   login_data.srv_diff_host_rate,
                   login_data.dst_host_count,
                   login_data.dst_host_srv_count,
                   login_data.dst_host_same_srv_rate,
                   login_data.dst_host_diff_srv_rate,
                   login_data.dst_host_same_src_port_rate,
                   login_data.dst_host_srv_diff_host_rate,
                   login_data.dst_host_serror_rate,
                   login_data.dst_host_srv_serror_rate,
                   login_data.dst_host_rerror_rate,
                   login_data.dst_host_srv_rerror_rate
                   ]]

        result = self.model.predict(sample).tolist()[0]
        return True if result == "normal" else False
