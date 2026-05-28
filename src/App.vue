<template>
  <el-container class="app-shell">
    <el-aside width="248px" class="sidebar">
      <div class="brand">
        <div class="brand-mark">从</div>
        <div>
          <div class="brand-title">产品套餐管理</div>
          <div class="brand-subtitle">产品套餐与能力维护</div>
        </div>
      </div>
      <el-menu :default-active="activeMenu" class="side-menu" @select="activeMenu = $event">
        <el-menu-item v-for="item in menus" :key="item.key" :index="item.key">{{ item.label }}</el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="topbar">
        <div>
          <div class="page-title">{{ currentMenu.label }}</div>
          <div class="page-desc">{{ currentMenu.desc }}</div>
        </div>
        <el-tag type="success" effect="plain">Mock 原型</el-tag>
      </el-header>

      <el-main class="page-main">
        <section v-show="activeMenu === 'overview'" class="page-stack">
          <div class="metric-grid">
            <div v-for="card in overviewCards" :key="card.label" class="metric-card">
              <span>{{ card.label }}</span>
              <strong>{{ card.value }}</strong>
              <em>{{ card.tip }}</em>
            </div>
          </div>

          <el-row :gutter="16">
            <el-col :span="16">
              <el-card shadow="never" class="content-card">
                <template #header><span>主体业务待办</span></template>
                <el-table :data="todos" height="300">
                  <el-table-column prop="subjectName" label="主体名称" min-width="190" />
                  <el-table-column prop="todo" label="待办事项" min-width="150" />
                  <el-table-column prop="packageName" label="当前套餐" min-width="140" />
                  <el-table-column prop="expire" label="到期时间" width="120" />
                  <el-table-column label="状态" width="96">
                    <template #default="{ row }"><StatusTag :status="row.status" /></template>
                  </el-table-column>
                  <el-table-column label="操作" width="110">
                    <template #default="{ row }">
                      <el-button link type="primary" @click="handleTodo(row)">处理</el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card shadow="never" class="content-card distribution-card">
                <template #header><span>套餐开通分布</span></template>
                <div v-for="item in distribution" :key="item.name" class="dist-row">
                  <div class="dist-head">
                    <span>{{ item.name }}</span>
                    <b>{{ item.count }}家</b>
                  </div>
                  <el-progress :percentage="item.percent" :show-text="false" />
                </div>
              </el-card>
            </el-col>
          </el-row>
        </section>

        <section v-show="activeMenu === 'packages'" class="page-stack">
          <el-card shadow="never" class="content-card">
            <SearchBar>
              <el-input v-model="packageFilter.name" placeholder="套餐名称" clearable />
              <el-select v-model="packageFilter.subject" placeholder="适用主体" clearable>
                <el-option label="企业" value="企业" />
                <el-option label="机构" value="培训机构" />
                <el-option label="集团" value="集团" />
              </el-select>
              <el-select v-model="packageFilter.status" placeholder="套餐状态" clearable>
                <el-option label="启用" value="启用" />
                <el-option label="停用" value="停用" />
              </el-select>
              <el-button type="primary" @click="openPackageForm()">新增套餐</el-button>
            </SearchBar>
            <el-table :data="paged(filteredPackages, packagePage)" border>
              <el-table-column prop="name" label="套餐名称" min-width="150" />
              <el-table-column prop="code" label="套餐编码" width="140" />
              <el-table-column prop="subject" label="适用主体" width="100" />
              <el-table-column prop="type" label="套餐类型" width="120" />
              <el-table-column label="默认期限" width="100"><template #default="{ row }">{{ row.duration }}个月</template></el-table-column>
              <el-table-column label="官方价格" width="120"><template #default="{ row }">{{ row.price }}元/年</template></el-table-column>
              <el-table-column label="续费价格" width="120"><template #default="{ row }">{{ row.renewPrice }}元/年</template></el-table-column>
              <el-table-column label="状态" width="90"><template #default="{ row }"><StatusTag :status="row.status" /></template></el-table-column>
              <el-table-column label="操作" width="260" fixed="right">
                <template #default="{ row }">
                  <el-button link type="primary" @click="openPackageDetail(row)">详情</el-button>
                  <el-button link type="primary" @click="openPackageForm(row)">编辑</el-button>
                  <el-button link type="primary" @click="copyPackage(row)">复制</el-button>
                  <el-button link :type="row.status === '启用' ? 'warning' : 'success'" @click="togglePackage(row)">{{ row.status === '启用' ? '停用' : '启用' }}</el-button>
                </template>
              </el-table-column>
            </el-table>
            <Pager v-model="packagePage" :total="filteredPackages.length" />
          </el-card>
        </section>

        <section v-show="activeMenu === 'abilities'" class="ability-layout">
          <el-card shadow="never" class="package-list-card">
            <template #header><span>套餐列表</span></template>
            <el-input v-model="abilityFilter.name" class="package-search" placeholder="搜索套餐名称" clearable />
            <div v-for="pkg in filteredAbilityPackages" :key="pkg.code" class="package-item" :class="{ active: selectedPackageCode === pkg.code }" @click="selectedPackageCode = pkg.code">
              <b>{{ pkg.name }}</b>
              <span>{{ pkg.subject }}</span>
              <StatusTag :status="pkg.status" />
            </div>
          </el-card>
          <el-card shadow="never" class="content-card ability-card">
            <template #header>
              <div class="card-header-line">
                <span>能力配置区</span>
                <div>
                  <el-select v-model="copyFromCode" placeholder="复制其他套餐能力" class="copy-select" clearable>
                    <el-option v-for="pkg in otherPackages" :key="pkg.code" :label="pkg.name" :value="pkg.code" />
                  </el-select>
                  <el-button @click="copyAbilities">复制</el-button>
                  <el-button @click="restoreAbilities">恢复默认</el-button>
                  <el-button type="primary" @click="saveAbilities">保存配置</el-button>
                </div>
              </div>
            </template>
            <div class="ability-summary">
              <span>当前套餐：<b>{{ selectedPackage.name }}</b></span>
              <span>适用主体：{{ selectedPackage.subject }}</span>
              <span>已选能力数量：{{ selectedAbilities.length }}</span>
              <span>最后更新时间：{{ abilityMeta[selectedPackageCode]?.updatedAt }}</span>
              <span>更新人：{{ abilityMeta[selectedPackageCode]?.operator }}</span>
            </div>
            <div class="ability-groups">
              <div v-for="group in abilityGroups" :key="group.key" class="ability-group">
                <div class="group-title">
                  <b>{{ group.name }}</b>
                  <el-button link type="primary" @click="selectGroup(group)">一键全选</el-button>
                </div>
                <el-checkbox-group v-model="selectedAbilities">
                  <el-checkbox v-for="ability in group.abilities" :key="ability" :label="ability" />
                </el-checkbox-group>
              </div>
            </div>
          </el-card>
        </section>

        <section v-show="activeMenu === 'open'" class="page-stack">
          <el-card shadow="never" class="content-card">
            <SearchBar>
              <el-input v-model="subjectFilter.name" placeholder="主体名称" clearable />
              <el-select v-model="subjectFilter.type" placeholder="主体类型" clearable>
                <el-option label="企业" value="企业" />
                <el-option label="机构" value="培训机构" />
                <el-option label="集团" value="集团" />
              </el-select>
              <el-select v-model="subjectFilter.status" placeholder="开通状态" clearable>
                <el-option label="使用中" value="使用中" />
                <el-option label="即将到期" value="即将到期" />
                <el-option label="已到期" value="已到期" />
                <el-option label="已停用" value="已停用" />
              </el-select>
              <el-button type="primary" @click="openActivation()">开通套餐</el-button>
            </SearchBar>
            <el-table :data="paged(filteredSubjects, subjectPage)" border>
              <el-table-column prop="name" label="主体名称" min-width="190" />
              <el-table-column prop="type" label="主体类型" width="110" />
              <el-table-column prop="packageName" label="当前套餐" min-width="150" />
              <el-table-column label="已开通能力" min-width="170"><template #default="{ row }">{{ row.abilities.join(' / ') }}</template></el-table-column>
              <el-table-column label="服务期限" min-width="210"><template #default="{ row }">{{ row.start }} ~ {{ row.end }}</template></el-table-column>
              <el-table-column label="开通状态" width="100"><template #default="{ row }"><StatusTag :status="serviceStatus(row)" /></template></el-table-column>
              <el-table-column label="操作" width="220" fixed="right">
                <template #default="{ row }">
                  <el-button link type="primary" @click="openActivation(row, '套餐变更')">变更套餐</el-button>
                  <el-button link type="primary" @click="openAppendAbility(row)">追加能力</el-button>
                  <el-button link type="primary" @click="openSubjectDetail(row)">详情</el-button>
                </template>
              </el-table-column>
            </el-table>
            <Pager v-model="subjectPage" :total="filteredSubjects.length" />
          </el-card>
        </section>

        <section v-show="activeMenu === 'service'" class="page-stack">
          <el-card shadow="never" class="content-card">
            <SearchBar>
              <el-input v-model="serviceFilter.name" placeholder="主体名称" clearable />
              <el-select v-model="serviceFilter.type" placeholder="主体类型" clearable>
                <el-option label="企业" value="企业" />
                <el-option label="机构" value="培训机构" />
                <el-option label="集团" value="集团" />
              </el-select>
              <el-select v-model="serviceFilter.status" placeholder="服务状态" clearable>
                <el-option label="使用中" value="使用中" />
                <el-option label="即将到期" value="即将到期" />
                <el-option label="已到期" value="已到期" />
                <el-option label="已停用" value="已停用" />
              </el-select>
            </SearchBar>
            <el-table :data="paged(filteredServices, servicePage)" border>
              <el-table-column prop="name" label="主体名称" min-width="190" />
              <el-table-column prop="type" label="主体类型" width="110" />
              <el-table-column prop="packageName" label="当前套餐" min-width="150" />
              <el-table-column prop="start" label="服务开始时间" width="130" />
              <el-table-column prop="end" label="服务结束时间" width="130" />
              <el-table-column label="剩余天数" width="100"><template #default="{ row }">{{ remainingDays(row) }}天</template></el-table-column>
              <el-table-column label="服务状态" width="100"><template #default="{ row }"><StatusTag :status="serviceStatus(row)" /></template></el-table-column>
              <el-table-column label="操作" width="240" fixed="right">
                <template #default="{ row }">
                  <el-button link type="primary" @click="openRenew(row)">套餐续费</el-button>
                  <el-button link type="primary" @click="openRenew(row, '延长服务')">延长服务</el-button>
                  <el-button v-if="!row.manualStopped" link type="warning" @click="stopService(row)">停用服务</el-button>
                  <el-button v-else link type="success" @click="resumeService(row)">恢复服务</el-button>
                </template>
              </el-table-column>
            </el-table>
            <Pager v-model="servicePage" :total="filteredServices.length" />
          </el-card>
        </section>

        <section v-show="activeMenu === 'records'" class="page-stack">
          <el-card shadow="never" class="content-card">
            <SearchBar>
              <el-input v-model="recordFilter.keyword" placeholder="业务单号 / 主体名称" clearable />
              <el-select v-model="recordFilter.bizType" placeholder="业务类型" clearable>
                <el-option v-for="type in bizTypes" :key="type" :label="type" :value="type" />
              </el-select>
              <el-select v-model="recordFilter.status" placeholder="状态" clearable>
                <el-option label="待确认" value="待确认" />
                <el-option label="已生效" value="已生效" />
                <el-option label="已取消" value="已取消" />
              </el-select>
            </SearchBar>
            <el-table :data="paged(filteredRecords, recordPage)" border>
              <el-table-column prop="no" label="业务单号" width="150" />
              <el-table-column prop="subjectName" label="主体名称" min-width="190" />
              <el-table-column prop="subjectType" label="主体类型" width="100" />
              <el-table-column prop="bizType" label="业务类型" width="110" />
              <el-table-column prop="content" label="业务内容" min-width="190" />
              <el-table-column prop="operator" label="经办人" width="130" />
              <el-table-column label="状态" width="96"><template #default="{ row }"><StatusTag :status="row.status" /></template></el-table-column>
              <el-table-column prop="createdAt" label="创建时间" width="160" />
              <el-table-column label="操作" width="90" fixed="right">
                <template #default="{ row }"><el-button link type="primary" @click="openRecordDetail(row)">详情</el-button></template>
              </el-table-column>
            </el-table>
            <Pager v-model="recordPage" :total="filteredRecords.length" />
          </el-card>
        </section>
      </el-main>
    </el-container>
  </el-container>

  <el-dialog v-model="packageDialog.visible" :title="packageDialog.title" width="720px">
    <el-form :model="packageForm" label-width="120px" class="dialog-form">
      <el-divider content-position="left">基础信息</el-divider>
      <el-form-item label="套餐名称"><el-input v-model="packageForm.name" /></el-form-item>
      <el-form-item label="套餐编码"><el-input v-model="packageForm.code" /></el-form-item>
      <el-form-item label="适用主体">
        <el-select v-model="packageForm.subject"><el-option label="企业" value="企业" /><el-option label="机构" value="培训机构" /><el-option label="集团" value="集团" /></el-select>
      </el-form-item>
      <el-form-item label="套餐类型">
        <el-select v-model="packageForm.type"><el-option label="基础套餐" value="基础套餐" /><el-option label="增强套餐" value="增强套餐" /><el-option label="集团套餐" value="集团套餐" /><el-option label="机构套餐" value="机构套餐" /></el-select>
      </el-form-item>
      <el-form-item label="默认服务期限"><el-select v-model="packageForm.duration"><el-option :value="6" label="6个月" /><el-option :value="12" label="12个月" /><el-option :value="24" label="24个月" /></el-select></el-form-item>
      <el-form-item label="官方价格"><el-input-number v-model="packageForm.price" :min="0" /></el-form-item>
      <el-form-item label="续费价格"><el-input-number v-model="packageForm.renewPrice" :min="0" /></el-form-item>
      <el-form-item label="排序"><el-input-number v-model="packageForm.sort" :min="1" /></el-form-item>
      <el-form-item label="状态"><el-radio-group v-model="packageForm.status"><el-radio-button label="启用" /><el-radio-button label="停用" /></el-radio-group></el-form-item>
      <el-form-item label="套餐说明"><el-input v-model="packageForm.desc" type="textarea" :rows="3" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="packageDialog.visible = false">取消</el-button>
      <el-button type="primary" @click="savePackage">确认</el-button>
    </template>
  </el-dialog>

  <el-dialog v-model="activationDialog.visible" :title="activationDialog.title" width="760px">
    <el-form :model="activationForm" label-width="120px" class="dialog-form">
      <el-form-item label="选择主体">
        <el-select v-model="activationForm.subjectId" filterable :disabled="activationDialog.lockSubject" @change="syncSubjectType">
          <el-option v-for="subject in subjects" :key="subject.id" :label="subject.name" :value="subject.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="主体类型"><el-input v-model="activationForm.subjectType" disabled /></el-form-item>
      <el-form-item label="选择套餐">
        <el-select v-model="activationForm.packageCode" @change="syncActivationPackage">
          <el-option v-for="pkg in packages" :key="pkg.code" :label="pkg.name" :value="pkg.code" />
        </el-select>
      </el-form-item>
      <el-form-item label="服务开始时间"><el-date-picker v-model="activationForm.start" value-format="YYYY-MM-DD" @change="calcActivationEnd" /></el-form-item>
      <el-form-item label="服务结束时间"><el-date-picker v-model="activationForm.end" value-format="YYYY-MM-DD" /></el-form-item>
      <el-form-item label="开通能力预览">
        <div class="tag-wall"><el-tag v-for="ability in activationAbilities" :key="ability" effect="plain">{{ ability }}</el-tag></div>
      </el-form-item>
      <el-form-item label="经办人"><el-input v-model="activationForm.operator" /></el-form-item>
      <el-form-item label="备注"><el-input v-model="activationForm.remark" type="textarea" :rows="3" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="activationDialog.visible = false">取消</el-button>
      <el-button type="primary" @click="confirmActivation">确认</el-button>
    </template>
  </el-dialog>

  <el-dialog v-model="appendDialog.visible" title="追加能力" width="720px">
    <div class="muted-line">主体：{{ appendDialog.subject?.name }} / 当前套餐：{{ appendDialog.subject?.packageName }}</div>
    <el-checkbox-group v-model="appendDialog.abilities" class="append-grid">
      <el-checkbox v-for="ability in allAbilities" :key="ability" :label="ability" />
    </el-checkbox-group>
    <template #footer>
      <el-button @click="appendDialog.visible = false">取消</el-button>
      <el-button type="primary" @click="confirmAppendAbility">确认追加</el-button>
    </template>
  </el-dialog>

  <el-dialog v-model="renewDialog.visible" :title="renewDialog.title" width="640px">
    <el-form :model="renewForm" label-width="120px" class="dialog-form">
      <el-form-item label="主体名称"><el-input v-model="renewForm.subjectName" disabled /></el-form-item>
      <el-form-item label="当前套餐"><el-input v-model="renewForm.packageName" disabled /></el-form-item>
      <el-form-item label="当前到期时间"><el-input v-model="renewForm.currentEnd" disabled /></el-form-item>
      <el-form-item label="续费周期"><el-select v-model="renewForm.months" @change="calcRenewEnd"><el-option :value="6" label="6个月" /><el-option :value="12" label="12个月" /><el-option :value="24" label="24个月" /></el-select></el-form-item>
      <el-form-item label="续费金额"><el-input-number v-model="renewForm.amount" :min="0" /></el-form-item>
      <el-form-item label="新到期时间"><el-input v-model="renewForm.newEnd" disabled /></el-form-item>
      <el-form-item label="经办人"><el-input v-model="renewForm.operator" /></el-form-item>
      <el-form-item label="备注"><el-input v-model="renewForm.remark" type="textarea" :rows="3" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="renewDialog.visible = false">取消</el-button>
      <el-button type="primary" @click="confirmRenew">确认</el-button>
    </template>
  </el-dialog>

  <el-drawer v-model="detailDrawer.visible" :title="detailDrawer.title" size="480px">
    <el-descriptions v-if="detailDrawer.data" :column="1" border>
      <el-descriptions-item v-for="item in detailItems" :key="item.label" :label="item.label">{{ item.value }}</el-descriptions-item>
    </el-descriptions>
  </el-drawer>
</template>

<script setup>
import { computed, defineComponent, h, reactive, ref, watch } from 'vue'
import { ElMessage, ElPagination, ElTag } from 'element-plus'
import { packageRows, subjectRows, recordRows } from './mock/packages'
import { abilityGroups, defaultPackageAbilities } from './mock/abilities'

const TODAY = new Date('2026-05-19T00:00:00')
const pageSize = 8

const StatusTag = defineComponent({
  props: { status: { type: String, required: true } },
  setup(props) {
    const typeMap = {
      启用: 'success',
      停用: 'info',
      使用中: 'success',
      即将到期: 'warning',
      已到期: 'danger',
      待确认: 'warning',
      待续费: 'warning',
      已生效: 'success',
      已取消: 'info',
      已停用: 'info'
    }
    return () => h(ElTag, { type: typeMap[props.status] || 'info', effect: 'light' }, () => props.status)
  }
})

const SearchBar = defineComponent({ setup(_, { slots }) { return () => h('div', { class: 'search-bar' }, slots.default?.()) } })
const Pager = defineComponent({
  props: { modelValue: Number, total: Number },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    return () => h('div', { class: 'pager' }, [
      h(ElPagination, {
        layout: 'total, prev, pager, next',
        total: props.total,
        pageSize,
        currentPage: props.modelValue,
        onCurrentChange: (page) => emit('update:modelValue', page)
      })
    ])
  }
})

const menus = [
  { key: 'overview', label: '套餐概览', desc: '快速查看套餐经营、服务到期与续费待办。' },
  { key: 'packages', label: '产品套餐', desc: '维护平台可售卖的产品套餐。' },
  { key: 'abilities', label: '套餐能力配置', desc: '按套餐维护平台能力范围。' },
  { key: 'open', label: '主体套餐开通', desc: '为已入驻主体开通、变更或追加能力。' },
  { key: 'service', label: '套餐服务管理', desc: '管理服务周期、到期状态和续费动作。' },
  { key: 'records', label: '开通续费记录', desc: '沉淀套餐开通、续费和能力变更记录。' }
]
const activeMenu = ref('overview')
const currentMenu = computed(() => menus.find((item) => item.key === activeMenu.value))

const packages = ref(structuredClone(packageRows))
const subjects = ref(structuredClone(subjectRows))
const records = ref(structuredClone(recordRows))
const packageAbilities = reactive(structuredClone(defaultPackageAbilities))
const abilityMeta = reactive(Object.fromEntries(packageRows.map((pkg) => [pkg.code, { updatedAt: '2026-05-18 16:30', operator: '平台运营-王五' }])))

const overviewCards = computed(() => [
  { label: '套餐数量', value: packages.value.length, tip: '当前可售卖套餐' },
  { label: '已开通主体', value: 86, tip: '含历史已开通主体' },
  { label: '即将到期主体', value: 8, tip: '30天内到期' },
  { label: '本月续费金额', value: '¥68,000', tip: '已生效续费单' }
])
const todos = computed(() => [
  { subjectName: '贵州XX煤矿有限公司', todo: '申请开通合同能力', packageName: '企业基础套餐', expire: '2026-05-20', status: '待确认', subject: subjects.value[0], action: 'append' },
  { subjectName: '贵州XX职业培训中心', todo: '套餐即将到期', packageName: '机构培训套餐', expire: '剩余18天', status: '待续费', subject: subjects.value[1], action: 'renew' }
])
const distribution = computed(() => {
  const data = [['企业基础套餐', 32], ['企业增强套餐', 18], ['集团协同套餐', 6], ['机构培训套餐', 30]]
  const max = Math.max(...data.map((item) => item[1]))
  return data.map(([name, count]) => ({ name, count, percent: Math.round((count / max) * 100) }))
})

const packageFilter = reactive({ name: '', subject: '', status: '' })
const subjectFilter = reactive({ name: '', type: '', status: '' })
const serviceFilter = reactive({ name: '', type: '', status: '' })
const recordFilter = reactive({ keyword: '', bizType: '', status: '' })
const abilityFilter = reactive({ name: '' })
const packagePage = ref(1)
const subjectPage = ref(1)
const servicePage = ref(1)
const recordPage = ref(1)
const bizTypes = ['套餐开通', '套餐续费', '套餐变更', '追加能力', '停用服务', '恢复服务']

const filteredPackages = computed(() => packages.value.filter((row) =>
  (!packageFilter.name || row.name.includes(packageFilter.name)) &&
  (!packageFilter.subject || row.subject === packageFilter.subject) &&
  (!packageFilter.status || row.status === packageFilter.status)
))
const filteredSubjects = computed(() => subjects.value.filter((row) =>
  (!subjectFilter.name || row.name.includes(subjectFilter.name)) &&
  (!subjectFilter.type || row.type === subjectFilter.type) &&
  (!subjectFilter.status || serviceStatus(row) === subjectFilter.status)
))
const filteredServices = computed(() => subjects.value.filter((row) =>
  (!serviceFilter.name || row.name.includes(serviceFilter.name)) &&
  (!serviceFilter.type || row.type === serviceFilter.type) &&
  (!serviceFilter.status || serviceStatus(row) === serviceFilter.status)
))
const filteredRecords = computed(() => records.value.filter((row) =>
  (!recordFilter.keyword || row.no.includes(recordFilter.keyword) || row.subjectName.includes(recordFilter.keyword)) &&
  (!recordFilter.bizType || row.bizType === recordFilter.bizType) &&
  (!recordFilter.status || row.status === recordFilter.status)
))

function paged(rows, page) {
  return rows.slice((page - 1) * pageSize, page * pageSize)
}

const selectedPackageCode = ref('ENT_BASIC')
const copyFromCode = ref('')
const selectedPackage = computed(() => packages.value.find((pkg) => pkg.code === selectedPackageCode.value) || packages.value[0])
const selectedAbilities = ref([...(packageAbilities[selectedPackageCode.value] || [])])
const otherPackages = computed(() => packages.value.filter((pkg) => pkg.code !== selectedPackageCode.value))
const filteredAbilityPackages = computed(() => packages.value.filter((pkg) => !abilityFilter.name || pkg.name.includes(abilityFilter.name)))
const allAbilities = computed(() => abilityGroups.flatMap((group) => group.abilities))

watch(selectedPackageCode, (code) => { selectedAbilities.value = [...(packageAbilities[code] || [])] })

function selectGroup(group) {
  selectedAbilities.value = Array.from(new Set([...selectedAbilities.value, ...group.abilities]))
}
function saveAbilities() {
  packageAbilities[selectedPackageCode.value] = [...selectedAbilities.value]
  abilityMeta[selectedPackageCode.value] = { updatedAt: '2026-05-19 15:30', operator: '平台运营-王五' }
  ElMessage.success('能力配置已保存')
}
function restoreAbilities() {
  selectedAbilities.value = [...(defaultPackageAbilities[selectedPackageCode.value] || [])]
  ElMessage.warning('已恢复默认能力配置')
}
function copyAbilities() {
  if (!copyFromCode.value) return ElMessage.warning('请选择要复制的套餐')
  selectedAbilities.value = [...(packageAbilities[copyFromCode.value] || [])]
  ElMessage.success('已复制套餐能力配置')
}

const packageDialog = reactive({ visible: false, title: '新增套餐', editingId: null })
const packageForm = reactive(blankPackage())
function blankPackage() {
  return { id: null, name: '', code: '', subject: '企业', type: '基础套餐', duration: 12, price: 0, renewPrice: 0, sort: 1, status: '启用', desc: '' }
}
function openPackageForm(row) {
  Object.assign(packageForm, row ? structuredClone(row) : blankPackage())
  packageDialog.editingId = row?.id || null
  packageDialog.title = row ? '编辑套餐' : '新增套餐'
  packageDialog.visible = true
}
function savePackage() {
  if (!packageForm.name || !packageForm.code) return ElMessage.warning('请填写套餐名称和套餐编码')
  if (packageDialog.editingId) {
    const index = packages.value.findIndex((row) => row.id === packageDialog.editingId)
    packages.value[index] = { ...packageForm }
  } else {
    packages.value.push({ ...packageForm, id: Date.now() })
    packageAbilities[packageForm.code] = []
    abilityMeta[packageForm.code] = { updatedAt: '-', operator: '-' }
  }
  packageDialog.visible = false
  ElMessage.success('套餐已保存')
}
function copyPackage(row) {
  const copy = { ...row, id: Date.now(), name: `${row.name} 副本`, code: `${row.code}_COPY`, status: '停用' }
  packages.value.push(copy)
  packageAbilities[copy.code] = [...(packageAbilities[row.code] || [])]
  abilityMeta[copy.code] = { updatedAt: '2026-05-19 15:30', operator: '平台运营-王五' }
  ElMessage.success('套餐已复制')
}
function togglePackage(row) {
  row.status = row.status === '启用' ? '停用' : '启用'
}

const activationDialog = reactive({ visible: false, title: '开通套餐', lockSubject: false })
const activationForm = reactive({ mode: '套餐开通', subjectId: null, subjectType: '', packageCode: 'ENT_BASIC', start: '2026-05-19', end: '2027-05-19', operator: '平台运营-王五', remark: '' })
const activationAbilities = computed(() => packageAbilities[activationForm.packageCode] || [])

function openActivation(row, mode = '套餐开通') {
  const subject = row || subjects.value[0]
  const pkg = packages.value.find((item) => item.code === subject.packageCode) || packages.value[0]
  Object.assign(activationForm, { mode, subjectId: subject.id, subjectType: subject.type, packageCode: pkg.code, start: '2026-05-19', end: addMonths('2026-05-19', pkg.duration), operator: '平台运营-王五', remark: '' })
  activationDialog.title = mode
  activationDialog.lockSubject = !!row
  activationDialog.visible = true
}
function syncSubjectType() {
  const subject = subjects.value.find((row) => row.id === activationForm.subjectId)
  activationForm.subjectType = subject?.type || ''
}
function syncActivationPackage() {
  calcActivationEnd()
}
function calcActivationEnd() {
  const pkg = packages.value.find((row) => row.code === activationForm.packageCode)
  activationForm.end = addMonths(activationForm.start, pkg?.duration || 12)
}
function confirmActivation() {
  const subject = subjects.value.find((row) => row.id === activationForm.subjectId)
  const pkg = packages.value.find((row) => row.code === activationForm.packageCode)
  if (!subject || !pkg) return
  const before = `${subject.packageName || '未开通'} ${subject.start || ''} ~ ${subject.end || ''}`
  Object.assign(subject, {
    packageCode: pkg.code,
    packageName: pkg.name,
    start: activationForm.start,
    end: activationForm.end,
    abilities: abilityNamesForSubject(activationAbilities.value),
    manualStopped: false
  })
  addRecord(subject, activationForm.mode, `${pkg.name}${activationForm.mode === '套餐开通' ? '开通' : '变更'}`, before, `${pkg.name} ${activationForm.start} ~ ${activationForm.end}`, activationForm.operator, '已生效', activationForm.remark)
  activationDialog.visible = false
  ElMessage.success(`${activationForm.mode}已生效`)
}

const appendDialog = reactive({ visible: false, subject: null, abilities: [] })
function openAppendAbility(row) {
  appendDialog.subject = row
  appendDialog.abilities = []
  appendDialog.visible = true
}
function confirmAppendAbility() {
  const subject = appendDialog.subject
  if (!subject) return
  const before = subject.abilities.join(' / ')
  subject.abilities = Array.from(new Set([...subject.abilities, ...abilityNamesForSubject(appendDialog.abilities)]))
  addRecord(subject, '追加能力', `新增${appendDialog.abilities.join('、') || '能力'}`, before, subject.abilities.join(' / '), '平台运营-王五', '待确认', '追加能力待业务确认。')
  appendDialog.visible = false
  ElMessage.success('追加能力记录已生成')
}

const renewDialog = reactive({ visible: false, title: '套餐续费' })
const renewForm = reactive({ subjectId: null, subjectName: '', packageName: '', currentEnd: '', months: 12, amount: 0, newEnd: '', operator: '运营财务-赵六', remark: '' })
function openRenew(row, title = '套餐续费') {
  const pkg = packages.value.find((item) => item.code === row.packageCode)
  Object.assign(renewForm, { subjectId: row.id, subjectName: row.name, packageName: row.packageName, currentEnd: row.end, months: 12, amount: pkg?.renewPrice || 0, newEnd: addMonths(row.end, 12), operator: '运营财务-赵六', remark: '' })
  renewDialog.title = title
  renewDialog.visible = true
}
function calcRenewEnd() {
  const subject = subjects.value.find((row) => row.id === renewForm.subjectId)
  const pkg = packages.value.find((row) => row.code === subject?.packageCode)
  renewForm.newEnd = addMonths(renewForm.currentEnd, renewForm.months)
  renewForm.amount = Math.round((pkg?.renewPrice || 0) * renewForm.months / 12)
}
function confirmRenew() {
  const subject = subjects.value.find((row) => row.id === renewForm.subjectId)
  if (!subject) return
  const before = `到期时间 ${subject.end}`
  subject.end = renewForm.newEnd
  subject.manualStopped = false
  addRecord(subject, renewDialog.title === '延长服务' ? '套餐变更' : '套餐续费', `${subject.packageName}续费${renewForm.months}个月`, before, `到期时间 ${subject.end}`, renewForm.operator, '已生效', renewForm.remark)
  renewDialog.visible = false
  ElMessage.success('服务期限已更新')
}
function stopService(row) {
  row.manualStopped = true
  addRecord(row, '停用服务', '人工停用服务', '使用中', '已停用', '平台运营-王五', '已生效', '')
}
function resumeService(row) {
  row.manualStopped = false
  addRecord(row, '恢复服务', '恢复主体套餐服务', '已停用', serviceStatus(row), '平台运营-王五', '已生效', '')
}
function handleTodo(row) {
  if (row.action === 'append') openAppendAbility(row.subject)
  else openRenew(row.subject)
}

const detailDrawer = reactive({ visible: false, title: '详情', data: null, kind: '' })
const detailItems = computed(() => {
  const row = detailDrawer.data
  if (!row) return []
  if (detailDrawer.kind === 'record') {
    return [
      ['业务单号', row.no], ['主体名称', row.subjectName], ['主体类型', row.subjectType], ['业务类型', row.bizType], ['业务内容', row.content], ['变更前', row.before], ['变更后', row.after], ['经办人', row.operator], ['状态', row.status], ['创建时间', row.createdAt], ['备注', row.remark]
    ].map(([label, value]) => ({ label, value }))
  }
  if (detailDrawer.kind === 'package') {
    return [
      ['套餐名称', row.name], ['套餐编码', row.code], ['适用主体', row.subject], ['套餐类型', row.type], ['默认期限', `${row.duration}个月`], ['官方价格', `${row.price}元/年`], ['续费价格', `${row.renewPrice}元/年`], ['状态', row.status], ['套餐说明', row.desc]
    ].map(([label, value]) => ({ label, value }))
  }
  return [
    ['主体名称', row.name], ['主体类型', row.type], ['当前套餐', row.packageName], ['已开通能力', row.abilities.join(' / ')], ['服务期限', `${row.start} ~ ${row.end}`], ['服务状态', serviceStatus(row)]
  ].map(([label, value]) => ({ label, value }))
})
function openRecordDetail(row) { detailDrawer.kind = 'record'; detailDrawer.title = '业务记录详情'; detailDrawer.data = row; detailDrawer.visible = true }
function openPackageDetail(row) { detailDrawer.kind = 'package'; detailDrawer.title = '套餐详情'; detailDrawer.data = row; detailDrawer.visible = true }
function openSubjectDetail(row) { detailDrawer.kind = 'subject'; detailDrawer.title = '主体套餐详情'; detailDrawer.data = row; detailDrawer.visible = true }

function remainingDays(row) {
  return Math.ceil((new Date(`${row.end}T00:00:00`) - TODAY) / 86400000)
}
function serviceStatus(row) {
  if (row.manualStopped) return '已停用'
  const days = remainingDays(row)
  if (days < 0) return '已到期'
  if (days <= 30) return '即将到期'
  return '使用中'
}
function addMonths(dateText, months) {
  const date = new Date(`${dateText}T00:00:00`)
  date.setMonth(date.getMonth() + Number(months))
  return date.toISOString().slice(0, 10)
}
function abilityNamesForSubject(abilities) {
  const names = new Set()
  abilities.forEach((ability) => {
    if (ability.includes('人员')) names.add('人员')
    if (ability.includes('培训') || ability.includes('学习') || ability.includes('学时')) names.add('培训')
    if (ability.includes('档案')) names.add('档案')
    if (ability.includes('合同')) names.add('合同')
    if (ability.includes('证书')) names.add('证书协同')
    if (ability.includes('考试') || ability.includes('题库') || ability.includes('成绩')) names.add('考试')
    if (ability.includes('主体') || ability.includes('汇总') || ability.includes('下钻') || ability.includes('协同')) names.add('集团协同')
  })
  return [...names]
}
function addRecord(subject, bizType, content, before, after, operator, status, remark) {
  records.value.unshift({
    id: Date.now(),
    no: `SV-20260519-${String(records.value.length + 1).padStart(3, '0')}`,
    subjectName: subject.name,
    subjectType: subject.type === '培训机构' ? '机构' : subject.type,
    bizType,
    content,
    before,
    after,
    operator,
    status,
    createdAt: '2026-05-19 15:30',
    remark
  })
}
</script>
