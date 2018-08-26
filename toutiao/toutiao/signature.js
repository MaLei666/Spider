function e(t) {
    var e = ascp.getHoney(),
    i = '';
    window.TAC && (i = TAC.sign('refresh' === t ? 0 : r.params.max_behot_time_tmp)),
    r.params = _.extend({
    }, r.params, {
      as: e.as,
      cp: e.cp,
      max_behot_time: 'refresh' === t ? 0 : r.params.max_behot_time_tmp,
      _signature: i
    })
  }