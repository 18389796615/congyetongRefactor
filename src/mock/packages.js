export const packageRows = [
  { id: 1, name: '企业基础套餐', code: 'ENT_BASIC', subject: '企业', type: '基础套餐', duration: 12, price: 999, renewPrice: 799, sort: 1, status: '启用', desc: '适合企业完成基础人员、培训与档案维护。' },
  { id: 2, name: '企业增强套餐', code: 'ENT_PLUS', subject: '企业', type: '增强套餐', duration: 12, price: 1999, renewPrice: 1599, sort: 2, status: '启用', desc: '面向需要合同能力和更完整数据维护的企业。' },
  { id: 3, name: '集团协同套餐', code: 'GROUP_COLLAB', subject: '集团', type: '集团套餐', duration: 12, price: 4999, renewPrice: 3999, sort: 3, status: '启用', desc: '支持集团管理下属主体和跨主体协同。' },
  { id: 4, name: '机构培训套餐', code: 'ORG_TRAIN', subject: '培训机构', type: '机构套餐', duration: 12, price: 2999, renewPrice: 2399, sort: 4, status: '启用', desc: '面向培训机构的培训、考试与证书协同能力。' }
]

export const subjectRows = [
  { id: 1, name: '贵州XX煤矿有限公司', type: '企业', packageCode: 'ENT_BASIC', packageName: '企业基础套餐', abilities: ['人员', '培训', '档案'], start: '2026-01-01', end: '2026-12-31', manualStopped: false },
  { id: 2, name: '贵州XX职业培训中心', type: '培训机构', packageCode: 'ORG_TRAIN', packageName: '机构培训套餐', abilities: ['培训', '考试', '证书协同'], start: '2025-06-01', end: '2026-06-01', manualStopped: false },
  { id: 3, name: '贵州能源集团', type: '集团', packageCode: 'GROUP_COLLAB', packageName: '集团协同套餐', abilities: ['集团协同', '汇总分析', '数据下钻'], start: '2026-03-01', end: '2027-02-28', manualStopped: false },
  { id: 4, name: '贵州安顺XX煤业', type: '企业', packageCode: 'ENT_PLUS', packageName: '企业增强套餐', abilities: ['人员', '培训', '档案', '合同'], start: '2025-05-01', end: '2026-05-25', manualStopped: false },
  { id: 5, name: '黔西南XX培训学校', type: '培训机构', packageCode: 'ORG_TRAIN', packageName: '机构培训套餐', abilities: ['培训', '考试'], start: '2024-12-01', end: '2026-04-30', manualStopped: false }
]

export const recordRows = [
  { id: 1, no: 'SV-20260518-004', subjectName: '贵州XX煤矿有限公司', subjectType: '企业', bizType: '追加能力', content: '新增合同能力', before: '人员 / 培训 / 档案', after: '人员 / 培训 / 档案 / 合同', operator: '平台运营-王五', status: '待确认', createdAt: '2026-05-18 14:20', remark: '客户已提交合同能力开通申请。' },
  { id: 2, no: 'SV-20260517-002', subjectName: '贵州XX职业培训中心', subjectType: '机构', bizType: '套餐续费', content: '机构培训套餐续费12个月', before: '到期时间 2026-06-01', after: '到期时间 2027-06-01', operator: '运营财务-赵六', status: '已生效', createdAt: '2026-05-17 09:40', remark: '线下款项已确认。' },
  { id: 3, no: 'SV-20260516-001', subjectName: '贵州能源集团', subjectType: '集团', bizType: '套餐开通', content: '开通集团协同套餐', before: '未开通', after: '集团协同套餐 12个月', operator: '平台运营-李四', status: '已生效', createdAt: '2026-05-16 11:10', remark: '集团主体首次开通。' }
]
